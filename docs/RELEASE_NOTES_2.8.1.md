# Codex Goal Supervisor 2.8.1

## Native Goal Synchronization

- Finalize reuse research and the detailed Goal contract before creating the native Codex Goal.
- Return a canonical native Goal payload contract with objective length and SHA-256.
- Require `create_goal` to consume the exact `goal_mode_objective` and `get_goal` to verify byte-for-byte equality before implementation.
- Treat an early rough-prompt Goal as unsynchronized; native `update_goal` changes status only and cannot repair its objective.

## Verification

- Added deterministic coverage for canonical payload length/hash and source-of-truth persistence.
- Strengthened the required real Luna Max black-box contract so early native Goal creation no longer qualifies as valid evidence.
