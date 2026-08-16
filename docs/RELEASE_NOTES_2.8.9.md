# Codex Goal Supervisor 2.8.9

## Candidate scope

- Replace a stale or blocked native Codex Goal without user UI operation.
- Preserve Goal history without falsely claiming that the superseded objective
  was completed.
- Keep existing observer, optional tools, feedback, and update behavior
  unchanged.

## Native Goal lifecycle

- `goal-set`, `phase-set`, and validated `phase-advance` use Codex app-server
  `thread/goal/set` with the finalized detailed objective.
- Every write is followed by `thread/goal/get`; objective bytes, length, hash,
  and active status must match before project Goal state commits.
- A replaced Goal is recorded in
  `.agent/goal_replacement_history.jsonl` as
  `SUPERSEDED_BY_USER_DIRECTION_CHANGE` with `objective_achieved=false`, prior
  status, prior usage, and old/new objective hashes.
- Bridge errors are bounded, kill the app-server process group, and leave the
  existing project Goal unchanged.

## Verification

- Added fake app-server lifecycle, timeout, rollback, replacement-history, and
  phased-advance regressions.
- A real run in `插件专用测试线程` replaced a blocked 76-character Goal with the
  3,326-character detailed Goal and independently verified the exact SHA-256.
- The local Codex build preserved cumulative usage counters during that real
  replacement despite current documentation describing reset semantics. The
  plugin does not depend on usage reset; objective and status are the verified
  authority.

## Release boundary

Publication requires schema-2 evidence bound to the exact clean commit. The
evidence must prove native replacement, exact read-back, durable replacement
history, and that the old Goal was not marked achieved before any network
write occurs.
