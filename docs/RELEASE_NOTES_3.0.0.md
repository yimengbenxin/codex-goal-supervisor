# Codex Goal Supervisor 3.0.0

Version: `3.0.0+codex.20260822135458`

## Product Change

V3 introduces one universal capability core with inherited runtime Profiles:

- `general-initial` is the explicit project baseline for ordinary Codex work. It does not require a North Star or native Goal.
- `goal-2.8.10-compatibility` inherits General and preserves the verified Goal behavior from 2.8.10.
- Capability availability, obligation, invocation, enforcement, and preconditions are distinct machine-readable dimensions.
- General requirements and targeted boundaries cannot be weakened by Goal Profile overrides.
- Optional Custodian, Company, Auditor, Janitor, Ticket, MDCP, and ledger tools remain optional.

## Bugs Fixed During Migration

- Goal replacement now archives and resets stale goal-scoped convergence state instead of leaving old and new segments active together.
- Detailed Goal research decisions that reject unsuitable reuse candidates persist into the project onboarding contract.
- Explicit activation checks the project runtime against the loaded plugin before first use and updates stale code without resetting project state.
- Runtime parity covers the complete installer-managed immutable tree, not only `goal_compass.py`.
- General Profile status no longer demands North Star confirmation for ordinary non-Goal work.
- Compact status keeps only the General Profile id; full compound policy statistics remain verbose-only.
- Dirty pre-release black boxes can use a content-aware worktree fingerprint; hashing `git status` path text is no longer treated as exact candidate evidence.
- Detailed Goal contracts can be checked with `goal-set --validate-only` before the single state-changing native Goal call.
- Final-certification identity now hashes stable authority-bearing Goal fields, so read-time defaults or a later successful validation event cannot falsely mark an unchanged Goal stale.
- General Profile now requires bounded instruction hygiene: completed temporary requests cannot recapture the primary task after repeated compaction, and recovery never re-injects their raw text.
- Resolved subtraction corrections now converge on the positive canonical result. Rejected variants cannot linger in PR/commit/tag wording, narrative files, or later completion summaries unless the user explicitly reopens them.
- Instruction-hygiene state is bounded and redacts credential-shaped text; hook events without turn IDs preserve only the correction response's one-time exemption.

## Verification Boundary

V3 is not publishable merely because deterministic tests pass. Release acceptance still requires:

1. the exact clean commit;
2. module and discover verification;
3. package selftest and extracted-edition checks;
4. the real Luna Max task named `插件专用测试线程`;
5. exact native/detailed Goal equality and independent product acceptance;
6. publication only after all prior evidence passes.

The historical under-60-second full-suite target remains open. Core tests were not deleted or skipped to manufacture a faster result.
