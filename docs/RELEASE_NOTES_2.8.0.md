# Codex Goal Supervisor 2.8.0

## Project procedure memory

- Each observed Codex task keeps one bounded, redacted local outcome summary.
- Successful deterministic commands are recorded without chat transcripts or private reasoning.
- A recognized local-service launch immediately creates a project-local Skill and an idempotent start/status/stop runner.
- Other fixed command sequences require matching success in two independent tasks before promotion.
- Generated procedures live under `.agent/procedures/**` and remain outside product diff budgets and Goal detection.
- `procedure` lists the compact index; `procedure --id <id>` returns one procedure contract.

## Noise and safety boundaries

- Ordinary read commands, one-off exploration, failed commands, temporary paths, credentials, arbitrary shell composition, and destructive operations are never materialized.
- Stored procedures are not injected into unrelated conversations. A future task loads only the matching project-local `SKILL.md`.
- Task summaries are local, bounded, redacted, and replaced per task identity instead of accumulating every Stop turn.
- Shared hook failure parsing now recognizes the `exit-code` spelling so a failed command cannot become reusable evidence.

## Verification

- Added local-service lifecycle coverage with a real loopback HTTP server.
- Added two-independent-task promotion coverage.
- Added sensitive/failed/read-only command rejection, false service-name, redaction, compact CLI, no-injection, install, status, and regression coverage.
