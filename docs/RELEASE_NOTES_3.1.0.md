# Codex Goal Supervisor 3.1.0

Version: `3.1.0+codex.20260822235720`

## Hierarchical Goal Workstreams

- A detailed parent Goal can define a generic workstream DAG for a super-large project.
- Only dependency-ready workstreams with disjoint writable paths can launch in parallel.
- Every workstream declares inputs, outputs, consumers, shared contracts, validation IDs, and its contribution to the parent Goal.
- The parent Codex task remains the North Star and integration owner; each child Codex task installs its own detailed native Goal without rewriting project-level North Star state.
- Child activation is atomically reserved so one workstream cannot be claimed by two tasks.
- Parent Goal changes make bound child workstreams stale and stop only further child product writes until reconciliation.
- Fanout is rejected unless expected time saved exceeds coordination and integration cost.
- Super-complex plans accept the canonical `goal_contribution` heading directly,
  avoiding duplicate prose added only to satisfy section detection.
- Unknown or non-executable child/final validation IDs now fail plan validation
  before any child task is created.

This is a Goal-mode execution tool, not a fixed department template or mandatory multi-task workflow.
