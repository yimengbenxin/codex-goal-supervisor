# Codex Goal Supervisor 2.6.1

This release fixes one unattended Goal-mode stop failure without adding a new
workflow or requiring user-managed tickets.

## External blocker recovery

- A local manual, device, login, or credential prerequisite no longer triggers
  only a generic Goal-wide review before Stop.
- The Stop hook now reads the detailed Goal dependency graph, excludes active
  and completed modules, and selects a dependency-ready unfinished module for
  immediate execution.
- The continuation message names the concrete Goal module and requires tool use
  rather than another planning-only response.
- A continuation with a product write, validation, or new evidence renews the
  alternate-path check so productive unattended work can continue.
- A planning-only continuation receives one bounded execution retry. A second
  no-progress stop is allowed so the Supervisor cannot create an infinite
  explanation loop.
- When no dependency-ready independent path exists, the genuine external
  prerequisite is allowed to stop the task normally.

## Verification

- Dependency-ready path selection is covered at the convergence-state level.
- Real Stop-hook sequences cover initial continuation, planning-only retry,
  bounded fail-open, productive renewal, and genuine global blockers.
- Source, discovery, selftest, and extracted-release verification are executed
  by the verified publisher before release assets are published.
