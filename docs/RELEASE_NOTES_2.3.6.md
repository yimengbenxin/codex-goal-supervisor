# Codex Goal Supervisor 2.3.6

## Why This Project Exists

Coding Agents are entering the Loop Era: they can work for hours, traverse large repositories, call tools, delegate work, survive context compaction, and iterate beyond a single conversation turn. The hard problem is no longer only generating a good next step. It is keeping thousands of locally reasonable steps aligned with one valuable outcome.

Long loops fail in recognizable ways. A temporary request can replace the real objective after compaction. Activity can grow while acceptance evidence stays flat. An Agent can repeat a failed path, optimize beyond completion, or produce structurally valid output that does not satisfy the product. A heavy supervisor can make the opposite mistake and consume more time than the rework it prevents.

Codex Goal Supervisor exists to solve that convergence problem.

> Its mission is to let an Agent work longer without becoming less aligned, move faster without hiding unfinished work, and recover from deviation without discarding useful progress.

It is a rational, low-noise administrator rather than a decision maker. The user and execution Agent retain judgment. The Supervisor preserves intent, observes evidence, detects expensive failure patterns, and intervenes only when the expected benefit exceeds the process cost.

## What 2.3.6 Delivers

- A concise, durable North Star separated from a concrete 2,000-3,500 character Goal-mode execution contract.
- Evidence-backed convergence state that distinguishes real progress from file, command, token, or subagent activity.
- Goal return after temporary requests and context compaction, preventing a completed side request from becoming an endless new loop.
- Persistent exact-deviation incidents with 30-minute rechecks, correction lanes, seven-day recurrence monitoring, and a sparse read-only LLM Judge before a targeted rail.
- Bounded context continuity for large reads without copying project source text into Supervisor state.
- Proportional verification and project-level final-regression certification before claiming the North Star complete.
- Optional Custodian, company roles, Auditor, Janitor, convergence records, and bounded tickets; ordinary work needs none of them.
- MARK_ONLY cleanup: product files are never automatically moved or deleted.
- Explicit project activation, local-only diagnostics by default, and three physically distinct distribution editions.

## Boundary

- No automatic enrollment of unrelated projects.
- No silent North Star rewriting and no replacement of user judgment.
- No mandatory ticket or role ceremony for ordinary work.
- No deletion or movement by Janitor.
- No diagnostic upload without explicit project consent.
- No semantic-guess blocking; uncertain or unavailable LLM judgment fails open.
- This is not a security sandbox, approval board, signature ledger, Agent OS, or corporate governance workflow.

The governing rule is simple: every intervention must create net execution benefit. A control that costs more than the likely rework it prevents stays inactive.

See the [Codex integration architecture](https://github.com/yimengbenxin/codex-goal-supervisor/blob/main/docs/ARCHITECTURE.md) for the complete lifecycle map, runtime flow, state boundary, and failure philosophy.

## Distribution editions

- **Offline**: choose it when the package must contain no network updater or feedback transport. Both are physically absent.
- **Update-only**: choose it when automatic updates are useful but remote feedback must be impossible from the installed package. Feedback upload/server code is physically absent.
- **Full**: choose it when automatic updates and optional redacted diagnostics are useful. Upload remains off by default and requires explicit consent for the current project.

The full and update-only editions use separate Git marketplaces. The updater rejects cross-edition replacement.

## Getting Started

Download the edition that matches the required network boundary from this release. From an extracted package, explicitly install the project runtime:

```bash
python3 scripts/install_governor.py /path/to/repo --force
```

Installation writes only `.agent/**` and `.codex/hooks.json`; it does not replace the project's README, AGENTS, or tests. Installing the plugin or an updater does not activate Goal Supervisor in every repository.

## Verification

- `python3 -m unittest -q verification.tests.test_goal_compass`: 435 tests passed in 75.910 seconds.
- `python3 -m unittest discover -s verification/tests -v`: 435 tests passed in 76.403 seconds.
- `python3 assets/governor-harness/.agent/selftest/test_goal_compass.py`: passed in 0.31 seconds.
- Python compilation checks passed for the runtime, installer, hook, release builder, updater, and verification tests.
- GitHub Actions passed the same 435-test suite and selftest on Ubuntu and Windows.
- Remote installation from both published Git marketplaces was verified in isolated `CODEX_HOME` directories.

The full verification suites pass, but their measured local duration is above the historical 60-second target. This release does not claim otherwise.

## Package Integrity

GitHub publishes the SHA256 digest beside each release asset. The release page also lists the three final digests outside the archives, avoiding a self-referential hash embedded inside the package being hashed.

## Third-party content

The optional expert-role library includes a pinned snapshot derived from `msitarzewski/agency-agents`; attribution and its MIT license are included in `NOTICE` and the bundled role-pack directory.
