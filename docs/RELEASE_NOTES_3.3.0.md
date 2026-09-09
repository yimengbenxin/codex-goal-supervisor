# Codex Supervisor 3.3.0

This candidate adds adaptive coding execution and bounded Subagent result
governance without making tickets or Subagents mandatory.

## Coding execution

- The main thread retains user-intent, architecture, integration, escalation,
  and final-acceptance ownership.
- Small, focused, tightly coupled, reversible, and read-only work may execute
  directly with no ticket and no Subagent.
- Independent, high-volume, mechanical, context-heavy, or separately
  verifiable work may use short-lived workers when delegation has positive net
  benefit.
- Luna Max is the preferred compatible high-volume coding worker. Explicit user
  choice and task-specific role routing remain valid.
- Repeated repair without new evidence stops after two attempts and returns
  root-cause ownership to the main thread.
- Token-stage percentages remain advisory observations rather than quotas or
  blocking thresholds.

## Subagent result context

- Project installation now registers both `SubagentStart` and `SubagentStop`.
- Workers receive a concise completion contract and return a bounded Result
  Capsule containing task/revision, execution state, `ACTION`, actual `VERIFY`,
  optional `ASSESS`, and an optional project-relative artifact path.
- Detailed invalid output is retained locally under
  `.agent/runtime/subagent_context/` and never uploaded automatically.
- `DONE` remains separate from root acceptance. Accepted worker capsules enter
  the registry as `UNREVIEWED`.
- Rework uses explicit `R2 | SUPERSEDES R1` sequencing; concurrent workers
  cannot claim the same task revision.
- Invalid output receives a bounded correction attempt. Retries are capped so
  the Hook cannot create an infinite Subagent loop.
- `status --verbose` exposes only the compact current-revision index.

## Host boundary

The current Codex Hook API exposes the Subagent final response and can continue
the Subagent, but it does not let a plugin replace the parent-visible payload;
`suppressOutput` is not implemented. This release enforces the strongest
bounded contract available through supported hooks and reports retry exhaustion
as unverified instead of claiming a transport-level guarantee.

## Verification

- Runtime refresh now generates project Hooks even with `--no-init`, preserving
  user Hooks, active tickets, and North Star state. Generated Hook contents are
  excluded from immutable source-file parity; missing owned events are checked
  separately so valid customized Hooks do not cause reinstall loops.
- File installation does not imply native project trust or Hook trust. Both
  must be checked before claiming runtime coverage.

- Added deterministic parsing, local artifact, authority, revision, retry, and
  20-worker concurrency coverage.
- Added installed repo-local Hook integration coverage.
- Full verification and extracted-package validation remain required before
  publication.
