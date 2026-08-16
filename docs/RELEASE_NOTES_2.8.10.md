# Codex Goal Supervisor 2.8.10

## Fixed

- Package selftest now unconditionally disables the native Goal bridge before
  loading Goal Compass. Release verification can no longer replace the Goal of
  the Codex task that launched the test with the neutral selftest objective.
- Added a real subprocess regression that supplies a host `CODEX_THREAD_ID`,
  explicitly enables the bridge, and points `CODEX_EXECUTABLE` at an invocation
  trap. The selftest must pass without invoking that trap.

## Scope

This patch changes only release/selftest isolation. Native unattended Goal
replacement for normal project commands remains unchanged: project `goal-set`,
`phase-set`, and `phase-advance` still use official app-server Goal methods and
verify the resulting objective before committing project state.

## Verification

Publication remains gated on source tests, extracted-package tests, selftest,
the fixed Luna Max black-box task, exact native Goal read-back, replacement
history, and independent product acceptance.
