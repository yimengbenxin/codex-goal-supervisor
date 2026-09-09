"""Bounded Subagent result contracts for the project-local Codex hook.

Codex owns the parent/child transport. This module uses the supported
SubagentStart and SubagentStop hooks to constrain the child-authored result,
record revisions, and keep detailed invalid output local to the project.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from .state_store import exclusive_file_lock, load_json, utc_now_iso, write_json


SCHEMA_VERSION = 1
DEFAULT_TARGET_CHARS = 720
DEFAULT_HARD_MAX_CHARS = 1200
DEFAULT_MAX_CORRECTIONS = 2
EXEC_STATES = {"DONE", "PARTIAL", "BLOCKED", "FAILED"}
ROOT_ACCEPTANCE_STATES = {"UNREVIEWED", "ACCEPTED", "REWORK_REQUIRED", "REJECTED"}
FORBIDDEN_AUTHORITY = ("SYSTEM_VERIFIED", "ROOT_ACCEPTED", "CANONICAL")
HEADER_RE = re.compile(
    r"^(?P<task>[A-Za-z0-9][A-Za-z0-9._-]{0,63})/R(?P<revision>[1-9][0-9]*)"
    r"\s*\|\s*(?P<state>DONE|PARTIAL|BLOCKED|FAILED)"
    r"(?:\s*\|\s*SUPERSEDES\s+R(?P<supersedes>[1-9][0-9]*))?$"
)
FIELD_RE = re.compile(r"^(ACTION|VERIFY|ASSESS|ARTIFACT):\s*(.*)$")


def _default_config() -> dict[str, Any]:
    return {
        "enabled": True,
        "mode": "bounded_capsule",
        "target_chars": DEFAULT_TARGET_CHARS,
        "hard_max_chars": DEFAULT_HARD_MAX_CHARS,
        "preserve_invalid_raw_result": True,
        "include_assess": True,
        "revision_tracking": True,
        "auto_read_artifact": False,
        "max_correction_attempts": DEFAULT_MAX_CORRECTIONS,
    }


def config(agent_dir: Path) -> dict[str, Any]:
    mode = load_json(agent_dir / "tool_mode.json", {})
    supplied = mode.get("subagent_context") if isinstance(mode, dict) else None
    result = _default_config()
    if isinstance(supplied, dict):
        result.update(supplied)
    result["target_chars"] = max(240, int(result.get("target_chars") or DEFAULT_TARGET_CHARS))
    result["hard_max_chars"] = max(
        result["target_chars"],
        int(result.get("hard_max_chars") or DEFAULT_HARD_MAX_CHARS),
    )
    result["max_correction_attempts"] = max(
        1, min(3, int(result.get("max_correction_attempts") or DEFAULT_MAX_CORRECTIONS))
    )
    return result


def empty_registry() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "agents": {},
        "tasks": {},
        "telemetry": [],
        "updated_at": None,
    }


def _load_registry(path: Path) -> dict[str, Any]:
    row = load_json(path, empty_registry())
    if not isinstance(row, dict):
        return empty_registry()
    row.setdefault("schema_version", SCHEMA_VERSION)
    row.setdefault("agents", {})
    row.setdefault("tasks", {})
    row.setdefault("telemetry", [])
    return row


def _bounded_identifier(value: Any, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value or "").strip()).strip("-._")
    return (text or fallback)[:64]


def _provisional_task_id(event: dict[str, Any]) -> str:
    seed = "|".join(
        str(event.get(key) or "")
        for key in ("session_id", "turn_id", "agent_id", "agent_type")
    )
    return "SA-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12].upper()


def _agent_record(event: dict[str, Any]) -> dict[str, Any]:
    agent_id = _bounded_identifier(event.get("agent_id"), "unknown-agent")
    return {
        "agent_id": agent_id,
        "agent_type": _bounded_identifier(event.get("agent_type"), "default"),
        "parent_session_id": str(event.get("session_id") or ""),
        "turn_id": str(event.get("turn_id") or ""),
        "provisional_task_id": _provisional_task_id(event),
        "provisional_revision": 1,
        "state": "RUNNING",
        "correction_attempts": 0,
        "started_at": utc_now_iso(),
    }


def start_context(
    agent_dir: Path,
    registry_path: Path,
    lock_path: Path,
    event: dict[str, Any],
) -> str | None:
    policy = config(agent_dir)
    if policy.get("enabled") is not True or policy.get("mode") != "bounded_capsule":
        return None
    record = _agent_record(event)
    try:
        with exclusive_file_lock(lock_path, timeout=0.2, stale_seconds=30.0):
            registry = _load_registry(registry_path)
            existing = registry["agents"].get(record["agent_id"])
            if isinstance(existing, dict):
                record = {**existing, "state": "RUNNING", "started_at": utc_now_iso()}
            registry["agents"][record["agent_id"]] = record
            registry["updated_at"] = utc_now_iso()
            write_json(registry_path, registry)
    except (OSError, RuntimeError, json.JSONDecodeError):
        return None
    task = record["provisional_task_id"]
    hard_max = policy["hard_max_chars"]
    return (
        "[Subagent result contract] Work in the shared workspace; keep logs and detail in a project-relative "
        "artifact. Your final response must contain only this capsule:\n"
        f"{task}/R1 | DONE|PARTIAL|BLOCKED|FAILED\n"
        "ACTION: what actually changed or inspected\n"
        "VERIFY: checks actually run and their result, or NOT_RUN\n"
        "ASSESS: optional short uncertain judgment\n"
        "ARTIFACT: optional project-relative path\n"
        f"Use an explicit TASK_ID/REV/SUPERSEDES from the assignment when supplied; otherwise use {task}/R1. "
        f"Keep the entire capsule at or below {hard_max} characters. DONE means execution ended, not correctness; "
        "do not return reasoning, full logs, full diffs, SYSTEM_VERIFIED, ROOT_ACCEPTED, or CANONICAL claims."
    )


def _safe_artifact_path(project_root: Path, raw: str) -> tuple[str | None, str | None]:
    value = raw.strip().replace("\\", "/")
    if not value:
        return None, None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        return None, "ARTIFACT must be a project-relative path without parent traversal"
    try:
        (project_root / Path(*path.parts)).resolve().relative_to(project_root.resolve())
    except ValueError:
        return None, "ARTIFACT resolves outside the project"
    return path.as_posix(), None


def parse_capsule(project_root: Path, text: str, *, hard_max_chars: int) -> tuple[dict[str, Any] | None, list[str]]:
    value = str(text or "").strip()
    errors: list[str] = []
    if not value:
        return None, ["final response is empty"]
    if len(value) > hard_max_chars:
        errors.append(f"capsule has {len(value)} characters; maximum is {hard_max_chars}")
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    header = HEADER_RE.fullmatch(lines[0]) if lines else None
    if not header:
        errors.append("first line must be TASK_ID/RN | EXEC_STATE with optional | SUPERSEDES RN")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        match = FIELD_RE.fullmatch(line)
        if not match:
            errors.append("capsule contains text outside ACTION/VERIFY/ASSESS/ARTIFACT fields")
            continue
        key, item = match.group(1), match.group(2).strip()
        if key in fields:
            errors.append(f"{key} may appear only once")
        fields[key] = item
    if not fields.get("ACTION"):
        errors.append("ACTION is required")
    if not fields.get("VERIFY"):
        errors.append("VERIFY is required and must state actual checks or NOT_RUN")
    if any(marker in value.upper() for marker in FORBIDDEN_AUTHORITY):
        errors.append("worker result may not claim system or root acceptance authority")
    artifact = None
    if fields.get("ARTIFACT"):
        artifact, artifact_error = _safe_artifact_path(project_root, fields["ARTIFACT"])
        if artifact_error:
            errors.append(artifact_error)
    if errors or not header:
        return None, list(dict.fromkeys(errors))
    revision = int(header.group("revision"))
    supersedes = int(header.group("supersedes")) if header.group("supersedes") else None
    if revision == 1 and supersedes is not None:
        errors.append("R1 cannot supersede an earlier revision")
    if revision > 1 and supersedes != revision - 1:
        errors.append(f"R{revision} must declare SUPERSEDES R{revision - 1}")
    if errors:
        return None, errors
    return {
        "task_id": header.group("task"),
        "revision": revision,
        "exec_state": header.group("state"),
        "supersedes": supersedes,
        "action": fields["ACTION"],
        "verify": fields["VERIFY"],
        "assess": fields.get("ASSESS"),
        "artifact": artifact,
        "capsule": value,
        "char_count": len(value),
    }, []


def _persist_invalid_raw(agent_dir: Path, agent: dict[str, Any], text: str) -> str | None:
    if not text:
        return None
    task = _bounded_identifier(agent.get("provisional_task_id"), "unknown-task")
    revision = int(agent.get("provisional_revision", 1) or 1)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    relative = Path("runtime") / "subagent_context" / "tasks" / task / f"R{revision}" / f"raw-final-{digest}.md"
    destination = agent_dir / relative
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    except OSError:
        return None
    return (Path(".agent") / relative).as_posix()


def _validate_revision(registry: dict[str, Any], capsule: dict[str, Any], agent_id: str) -> list[str]:
    task_id = capsule["task_id"]
    revision = capsule["revision"]
    task = registry["tasks"].get(task_id)
    if not isinstance(task, dict):
        return [] if revision == 1 else [f"{task_id}/R1 is not registered; a new task must start at R1"]
    current = int(task.get("current_revision", 0) or 0)
    revisions = task.get("revisions") if isinstance(task.get("revisions"), dict) else {}
    existing = revisions.get(str(revision))
    if isinstance(existing, dict) and existing.get("agent_id") != agent_id:
        return [f"{task_id}/R{revision} already belongs to another worker"]
    if revision == current:
        if isinstance(existing, dict) and existing.get("capsule") != capsule.get("capsule"):
            return [f"{task_id}/R{revision} is already recorded; changed results require R{current + 1} | SUPERSEDES R{current}"]
        return []
    if revision != current + 1 or capsule.get("supersedes") != current:
        return [f"{task_id} current revision is R{current}; next result must be R{current + 1} | SUPERSEDES R{current}"]
    return []


def _record_valid(
    registry: dict[str, Any],
    capsule: dict[str, Any],
    agent: dict[str, Any],
    observed_at: str,
) -> None:
    task_id = capsule["task_id"]
    revision = capsule["revision"]
    task = registry["tasks"].setdefault(task_id, {"current_revision": 0, "revisions": {}})
    revisions = task.setdefault("revisions", {})
    if str(revision) in revisions:
        # A repeated delivery must not reset acceptance or replace prior evidence.
        return
    previous = capsule.get("supersedes")
    if previous is not None:
        old = revisions.get(str(previous))
        if isinstance(old, dict):
            old["superseded_by"] = revision
    revisions[str(revision)] = {
        **capsule,
        "agent_id": agent["agent_id"],
        "agent_type": agent.get("agent_type"),
        "root_acceptance": "UNREVIEWED",
        "verification_source": "worker_report",
        "runtime_verification": "UNVERIFIED",
        "completed_at": observed_at,
    }
    task["current_revision"] = revision
    task["updated_at"] = observed_at
    agent.update({
        "state": capsule["exec_state"],
        "task_id": task_id,
        "revision": revision,
        "completed_at": observed_at,
    })


def _retry_reason(agent: dict[str, Any], errors: list[str], artifact: str | None, hard_max: int) -> str:
    task = agent.get("provisional_task_id") or "TASK"
    detail = "; ".join(errors[:3])
    artifact_note = f" Detailed previous output is local at {artifact}." if artifact else ""
    return (
        "[Return a bounded Result Capsule] Your previous final result did not satisfy the parent context contract: "
        f"{detail}. Preserve the assigned task ID and revision (including SUPERSEDES for rework); "
        f"use {task}/R1 only when none was assigned. Return separate lines for the header and ACTION: actual work; "
        "VERIFY: checks and results or NOT_RUN; optional ASSESS and ARTIFACT. "
        f"Maximum {hard_max} characters. Do not include reasoning, logs, diffs, or system-level acceptance claims."
        + artifact_note
    )


def stop_decision(
    project_root: Path,
    agent_dir: Path,
    registry_path: Path,
    lock_path: Path,
    event: dict[str, Any],
) -> dict[str, Any]:
    policy = config(agent_dir)
    if policy.get("enabled") is not True or policy.get("mode") != "bounded_capsule":
        return {"action": "accept", "status": "DISABLED"}
    agent_id = _bounded_identifier(event.get("agent_id"), "unknown-agent")
    text = str(event.get("last_assistant_message") or "").strip()
    observed_at = utc_now_iso()
    try:
        with exclusive_file_lock(lock_path, timeout=0.3, stale_seconds=30.0):
            registry = _load_registry(registry_path)
            agent = registry["agents"].get(agent_id)
            if not isinstance(agent, dict):
                agent = _agent_record(event)
                registry["agents"][agent_id] = agent
            capsule, errors = parse_capsule(
                project_root,
                text,
                hard_max_chars=policy["hard_max_chars"],
            )
            if capsule:
                errors.extend(_validate_revision(registry, capsule, agent_id))
            if capsule and not errors:
                _record_valid(registry, capsule, agent, observed_at)
                telemetry = {
                    "agent_id": agent_id,
                    "task_id": capsule["task_id"],
                    "revision": capsule["revision"],
                    "raw_char_count": len(text),
                    "capsule_char_count": len(text),
                    "normalized": True,
                    "truncated": False,
                    "root_acceptance": "UNREVIEWED",
                    "observed_at": observed_at,
                }
                registry["telemetry"] = [*registry.get("telemetry", []), telemetry][-100:]
                registry["updated_at"] = observed_at
                write_json(registry_path, registry)
                return {"action": "accept", "status": "CAPSULE_ACCEPTED", "capsule": capsule}

            artifact = None
            if policy.get("preserve_invalid_raw_result") is True:
                artifact = _persist_invalid_raw(agent_dir, agent, text)
            attempts = int(agent.get("correction_attempts", 0) or 0) + 1
            agent["correction_attempts"] = attempts
            agent["state"] = "RESULT_CORRECTION_REQUIRED"
            agent["last_errors"] = errors[:5]
            agent["last_raw_artifact"] = artifact
            agent["updated_at"] = observed_at
            registry["telemetry"] = [*registry.get("telemetry", []), {
                "agent_id": agent_id,
                "task_id": agent.get("provisional_task_id"),
                "revision": agent.get("provisional_revision", 1),
                "raw_char_count": len(text),
                "capsule_char_count": 0,
                "normalized": False,
                "truncated": len(text) > policy["hard_max_chars"],
                "artifact_persisted": bool(artifact),
                "observed_at": observed_at,
            }][-100:]
            registry["updated_at"] = observed_at
            write_json(registry_path, registry)
            reason = _retry_reason(agent, errors, artifact, policy["hard_max_chars"])
            if attempts <= policy["max_correction_attempts"]:
                return {"action": "retry", "status": "CAPSULE_CORRECTION_REQUIRED", "reason": reason}
            return {
                "action": "warn",
                "status": "CAPSULE_RETRY_EXHAUSTED",
                "reason": (
                    "Subagent result remained outside the bounded capsule contract after the allowed correction attempts. "
                    "Treat it as an unverified worker report and inspect workspace evidence before acceptance."
                ),
            }
    except (OSError, RuntimeError, json.JSONDecodeError) as exc:
        return {
            "action": "warn",
            "status": "CAPSULE_GATE_UNAVAILABLE",
            "reason": f"Subagent result registry unavailable: {type(exc).__name__}. Treat the worker report as unverified.",
        }


def compact_status(registry_path: Path) -> dict[str, Any]:
    registry = _load_registry(registry_path)
    tasks = registry.get("tasks") if isinstance(registry.get("tasks"), dict) else {}
    current = []
    for task_id, task in sorted(tasks.items()):
        if not isinstance(task, dict):
            continue
        revision = int(task.get("current_revision", 0) or 0)
        row = task.get("revisions", {}).get(str(revision), {}) if revision else {}
        current.append({
            "task_id": task_id,
            "current_revision": revision,
            "exec_state": row.get("exec_state"),
            "root_acceptance": row.get("root_acceptance"),
            "artifact": row.get("artifact"),
        })
    return {
        "task_count": len(current),
        "current": current[-20:],
        "telemetry_count": len(registry.get("telemetry", [])),
    }
