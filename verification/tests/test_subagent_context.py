from __future__ import annotations

import concurrent.futures
import json
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from .helpers import HARNESS_ROOT
except ImportError:
    from helpers import HARNESS_ROOT


AGENT_SOURCE = HARNESS_ROOT / ".agent"
if str(AGENT_SOURCE) not in sys.path:
    sys.path.insert(0, str(AGENT_SOURCE))

from goal_compass_runtime.subagent_context import (  # noqa: E402
    parse_capsule,
    start_context,
    stop_decision,
)


class SubagentContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.agent = self.root / ".agent"
        self.registry = self.agent / "runtime" / "subagent_context" / "registry.json"
        self.lock = self.agent / "runtime" / "subagent_context" / "registry.lock"
        self.agent.mkdir(parents=True)
        (self.agent / "tool_mode.json").write_text(json.dumps({
            "subagent_context": {
                "enabled": True,
                "mode": "bounded_capsule",
                "target_chars": 720,
                "hard_max_chars": 1200,
                "max_correction_attempts": 2,
                "preserve_invalid_raw_result": True,
            }
        }), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def event(self, agent_id: str, *, message: str | None = None, active: bool = False) -> dict:
        row = {
            "session_id": "parent-session",
            "turn_id": "parent-turn",
            "cwd": str(self.root),
            "agent_id": agent_id,
            "agent_type": "worker",
            "stop_hook_active": active,
        }
        if message is not None:
            row["last_assistant_message"] = message
        return row

    def test_start_context_assigns_bounded_result_contract(self) -> None:
        text = start_context(self.agent, self.registry, self.lock, self.event("agent-1"))

        self.assertIn("Subagent result contract", text)
        self.assertIn("ACTION:", text)
        self.assertIn("VERIFY:", text)
        self.assertIn("DONE means execution ended, not correctness", text)
        self.assertLess(len(text), 1200)

    def test_done_capsule_remains_unreviewed(self) -> None:
        context = start_context(self.agent, self.registry, self.lock, self.event("agent-1"))
        task_id = context.splitlines()[1].split("/R1", 1)[0]
        message = (
            f"{task_id}/R1 | DONE\n"
            "ACTION: changed retry handling in src/client.py\n"
            "VERIFY: 3/3 targeted tests PASS; full suite NOT_RUN\n"
            "ASSESS: likely resolves the reported retry loop"
        )

        result = stop_decision(self.root, self.agent, self.registry, self.lock, self.event("agent-1", message=message))
        state = json.loads(self.registry.read_text(encoding="utf-8"))
        current = state["tasks"][task_id]["revisions"]["1"]

        self.assertEqual(result["status"], "CAPSULE_ACCEPTED")
        self.assertEqual(current["exec_state"], "DONE")
        self.assertEqual(current["root_acceptance"], "UNREVIEWED")
        self.assertNotEqual(current["root_acceptance"], "ACCEPTED")

    def test_long_free_text_is_preserved_locally_and_retried(self) -> None:
        start_context(self.agent, self.registry, self.lock, self.event("agent-long"))
        message = "I completed everything. " + ("full log and reasoning " * 300)

        result = stop_decision(
            self.root,
            self.agent,
            self.registry,
            self.lock,
            self.event("agent-long", message=message),
        )
        state = json.loads(self.registry.read_text(encoding="utf-8"))
        agent = state["agents"]["agent-long"]

        self.assertEqual(result["action"], "retry")
        self.assertEqual(result["status"], "CAPSULE_CORRECTION_REQUIRED")
        self.assertNotIn(message, result["reason"])
        self.assertTrue(agent["last_raw_artifact"].startswith(".agent/runtime/subagent_context/tasks/"))
        self.assertTrue((self.root / agent["last_raw_artifact"]).is_file())

    def test_revision_supersedes_only_current_revision(self) -> None:
        start_context(self.agent, self.registry, self.lock, self.event("agent-r1"))
        first = (
            "TASK-173/R1 | DONE\n"
            "ACTION: changed lock ordering\n"
            "VERIFY: targeted tests PASS; integration NOT_RUN"
        )
        self.assertEqual(
            stop_decision(self.root, self.agent, self.registry, self.lock, self.event("agent-r1", message=first))["action"],
            "accept",
        )

        start_context(self.agent, self.registry, self.lock, self.event("agent-r2"))
        second = (
            "TASK-173/R2 | DONE | SUPERSEDES R1\n"
            "ACTION: reverted R1 and moved synchronization to the coordinator\n"
            "VERIFY: 18/18 targeted tests PASS; full suite PASS"
        )
        self.assertEqual(
            stop_decision(self.root, self.agent, self.registry, self.lock, self.event("agent-r2", message=second))["action"],
            "accept",
        )
        task = json.loads(self.registry.read_text(encoding="utf-8"))["tasks"]["TASK-173"]

        self.assertEqual(task["current_revision"], 2)
        self.assertEqual(task["revisions"]["1"]["root_acceptance"], "UNREVIEWED")
        self.assertEqual(task["revisions"]["1"]["superseded_by"], 2)
        self.assertEqual(task["revisions"]["2"]["root_acceptance"], "UNREVIEWED")

    def test_duplicate_delivery_preserves_root_acceptance(self) -> None:
        message = "T1/R1 | DONE\nACTION: inspected input\nVERIFY: NOT_RUN"
        event = self.event("worker", message=message)
        stop_decision(self.root, self.agent, self.registry, self.lock, event)
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        record = registry["tasks"]["T1"]["revisions"]["1"]
        record["root_acceptance"] = "ACCEPTED"
        self.registry.write_text(json.dumps(registry), encoding="utf-8")
        result = stop_decision(self.root, self.agent, self.registry, self.lock, event)
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["tasks"]["T1"]["revisions"]["1"]
        self.assertEqual(result["action"], "accept")
        self.assertEqual(saved["root_acceptance"], "ACCEPTED")
        self.assertEqual(saved["runtime_verification"], "UNVERIFIED")

    def test_changed_same_revision_cannot_overwrite_result(self) -> None:
        first = "T1/R1 | DONE\nACTION: inspected input\nVERIFY: NOT_RUN"
        stop_decision(self.root, self.agent, self.registry, self.lock, self.event("worker", message=first))
        result = stop_decision(self.root, self.agent, self.registry, self.lock,
                               self.event("worker", message=first.replace("NOT_RUN", "all tests PASS")))
        self.assertEqual(result["action"], "retry")
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["tasks"]["T1"]["revisions"]["1"]
        self.assertEqual(saved["verify"], "NOT_RUN")

    def test_late_old_revision_cannot_replace_current(self) -> None:
        first = "T1/R1 | DONE\nACTION: inspected input\nVERIFY: NOT_RUN"
        second = "T1/R2 | DONE | SUPERSEDES R1\nACTION: fixed input\nVERIFY: focused check PASS"
        stop_decision(self.root, self.agent, self.registry, self.lock, self.event("worker1", message=first))
        stop_decision(self.root, self.agent, self.registry, self.lock, self.event("worker2", message=second))
        result = stop_decision(self.root, self.agent, self.registry, self.lock, self.event("worker1", message=first))
        self.assertNotEqual(result["action"], "accept")
        saved = json.loads(self.registry.read_text(encoding="utf-8"))["tasks"]["T1"]
        self.assertEqual(saved["current_revision"], 2)

    def test_invalid_capsule_retry_is_bounded(self) -> None:
        start_context(self.agent, self.registry, self.lock, self.event("agent-invalid"))
        results = [
            stop_decision(
                self.root,
                self.agent,
                self.registry,
                self.lock,
                self.event("agent-invalid", message="unstructured result", active=index > 0),
            )
            for index in range(3)
        ]

        self.assertEqual([row["action"] for row in results], ["retry", "retry", "warn"])
        self.assertEqual(results[-1]["status"], "CAPSULE_RETRY_EXHAUSTED")

    def test_forbidden_authority_and_outside_artifact_are_rejected(self) -> None:
        message = (
            "TASK-1/R1 | DONE\n"
            "ACTION: changed one file\n"
            "VERIFY: SYSTEM_VERIFIED\n"
            "ARTIFACT: ../outside.log"
        )

        capsule, errors = parse_capsule(self.root, message, hard_max_chars=1200)

        self.assertIsNone(capsule)
        self.assertTrue(any("authority" in row for row in errors))
        self.assertTrue(any("project-relative" in row for row in errors))

    def test_twenty_concurrent_subagents_do_not_mix_tasks(self) -> None:
        def execute(index: int) -> tuple[str, str]:
            agent_id = f"agent-{index:02d}"
            context = start_context(self.agent, self.registry, self.lock, self.event(agent_id))
            task_id = context.splitlines()[1].split("/R1", 1)[0]
            message = (
                f"{task_id}/R1 | DONE\n"
                f"ACTION: inspected module {index}\n"
                f"VERIFY: focused check {index} PASS"
            )
            result = stop_decision(self.root, self.agent, self.registry, self.lock, self.event(agent_id, message=message))
            return task_id, result["status"]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            rows = list(pool.map(execute, range(20)))
        state = json.loads(self.registry.read_text(encoding="utf-8"))

        self.assertEqual(len({task_id for task_id, _ in rows}), 20)
        self.assertTrue(all(status == "CAPSULE_ACCEPTED" for _, status in rows))
        self.assertEqual(len(state["tasks"]), 20)
        self.assertEqual(len(state["agents"]), 20)


if __name__ == "__main__":
    unittest.main()
