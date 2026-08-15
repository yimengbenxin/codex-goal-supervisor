# Codex Goal Supervisor 2.8.2

## Release Order Enforcement

- Require a real Luna Max black-box run before publication, bound to the exact clean release commit and plugin version.
- Require exact SHA-256 equality between the detailed plugin Goal and the native Codex Goal read back through `get_goal`.
- Reject release evidence when native Goal creation happened before detailed Goal finalization, online reuse research did not run, or independent product acceptance failed.
- Keep source tests, extracted-ZIP tests, packaging, network publication, and remote read-back after the real black box instead of using publication as a test step.

## Native Goal Synchronization

- Preserve the 2.8.1 fix that makes `goal_mode_objective` the canonical native Goal payload.
- Keep `update_goal` limited to lifecycle status; it is never treated as an objective-edit mechanism.
