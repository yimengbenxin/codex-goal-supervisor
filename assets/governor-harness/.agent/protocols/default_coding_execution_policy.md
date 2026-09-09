# Default Coding Execution Policy

This policy applies only after Codex Supervisor is explicitly activated for a
project. It refines coding execution; it does not force every task into tickets,
company mode, or visible governance.

## Net-benefit routing

- The main thread owns user intent, architecture decisions, dependency order,
  conflict resolution, integration, and final acceptance.
- The main thread may execute a small, focused, tightly coupled, or reversible
  change directly when delegation would cost more than it saves.
- Delegate when work is independently executable, high-volume, mechanically
  repetitive, context-heavy, or benefits from an independent verification view.
- A ticket is optional. A Subagent assignment may use the same compact fields
  without creating a persisted ticket.
- Read-only work, status checks, and tiny fixes require neither a ticket nor a
  Subagent merely because the capability exists.

## Assignment contract

Give each Subagent only the context needed for its assignment:

1. task id and revision when this is rework;
2. goal and expected business result;
3. relevant inputs, files, modules, and upstream artifacts;
4. writable and read-only boundaries;
5. interfaces, invariants, and dependencies;
6. required assertions and validation;
7. artifact destination;
8. escalation and stop conditions.

Do not send the complete main-thread history by default. Do not ask a worker to
rediscover the whole architecture when the parent already knows the relevant
contract.

## Execution model

- `Luna Max` is the preferred default for high-volume coding execution when it
  is available and compatible.
- The user may choose another model. Codex Supervisor may select another
  compatible model when task-specific capability or a company-role contract
  requires it.
- Model choice is not a completion signal. Workspace state and executed
  validation remain the evidence.

## Workflow

Use the smallest lifecycle justified by the work:

1. understand the requested outcome;
2. inspect only necessary context;
3. plan the expensive or cross-module portion;
4. research reuse when the route is not already established;
5. execute directly or delegate bounded assignments;
6. capture actual changes and validation evidence;
7. review according to risk;
8. repair with a new hypothesis when required;
9. run the smallest meaningful regression;
10. claim completion only from evidence.

The lifecycle may be implicit. Do not create ceremony solely to prove it was
followed.

## Retry and escalation

- A failed attempt must produce new evidence, a new reproduction, a new causal
  hypothesis, a new constraint, or a materially different repair strategy.
- Two failed repair attempts against the same assertion without new evidence
  stop autonomous retry and return the root-cause decision to the main thread.
- Routine, localized causes may be repaired by the worker. Cross-module,
  intermittent, interface-changing, or causally unclear failures return to the
  main thread for diagnosis.
- Do not relabel the same retry as a new route.

## Verification

- Define critical correctness as assertions before or during implementation.
- Workers run focused tests and report only checks actually executed.
- Small changes use focused verification. Cross-cutting and release-sensitive
  changes use the affected regression set.
- Do not rerun a broad suite after every micro-edit without new risk or change.
- `DONE` means the worker stopped executing. It never means the result is
  accepted, verified, releasable, or complete at the project level.

## Context isolation

- Detailed logs, reports, diffs, and research live in the workspace or a
  project-relative artifact.
- The worker returns one bounded Result Capsule.
- The main thread starts with the capsule, then reads status, focused diff,
  relevant sections, or artifacts only when the next decision needs them.
- Full Subagent reasoning and full process history are never the default return.

## Result Capsule

```text
TASK_ID/RN | DONE|PARTIAL|BLOCKED|FAILED | optional SUPERSEDES RN
ACTION: work actually performed
VERIFY: checks actually run and result, or NOT_RUN
ASSESS: optional short worker judgment with uncertainty
ARTIFACT: optional project-relative path
```

The capsule must stay within the configured context limit. `VERIFY` has higher
retention priority than `ASSESS`. A worker may not claim `SYSTEM_VERIFIED`,
`ROOT_ACCEPTED`, or `CANONICAL` status.

## Rework

- Rework of the same task increments the revision.
- `R2` must state `SUPERSEDES R1`; `R3` must state `SUPERSEDES R2`.
- The latest valid unsuperseded revision is current.
- Older revisions remain history and cannot overwrite the current result.
- Worker execution state and root acceptance state are separate.

## Parallel work

- Parallelize only independent work with stable shared contracts and disjoint
  write ownership.
- Keep dependent work serial.
- Different tasks have independent revisions.
- The same task revision has one writer unless an explicit candidate-merge
  contract already exists.

## Token and activity telemetry

Token-share percentages are planning observations, never quotas or hard gates.
Investigate only when activity grows without proportional acceptance evidence.
Do not create warnings merely because a numerical share differs from a generic
baseline.

## Completion

Completion requires the requested behavior, relevant assertions, executed
validation, no unresolved high-severity finding, and explicit disclosure of
anything unverified. The main thread remains the sole integration and final
acceptance authority.
