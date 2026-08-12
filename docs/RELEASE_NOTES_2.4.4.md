# Codex Goal Supervisor 2.4.4

This patch closes two low-noise Goal-direction confirmation gaps found during
realistic installed-project regression.

## Fixes

- A pending durable direction change is now project-scoped for the current Goal
  generation. Context compaction or a new session cannot repeat the same prompt
  or prevent the user's confirmation from resolving it.
- Questions that merely mention confirmation, such as asking why a North Star
  update is needed, remain questions and cannot be mistaken for confirmation.
- Session identity remains diagnostic provenance only; it is not authority for
  the project's confirmed North Star.

## Business Regression

- Verified an uninstalled project stays silent and installation preserves the
  project's README, AGENTS, and tests.
- Verified feedback remains local-only by default.
- Verified a 3,024-character detailed Goal contract, temporary-request silence,
  contained-subgoal silence, cross-session direction confirmation, external
  prerequisite recovery, and confidence-routed expert input.
- Verified the offline, update-only, and full editions remain physically
  distinct.

## Verification

- Installed-project business matrix: 16 scenarios passed.
- Focused feature regression: 133 tests passed in 27.70 seconds.
- Source module suite: 463 tests passed in 73.28 seconds.
- Source discovery suite: 463 tests passed in 74.20 seconds.
- Extracted full-ZIP module suite: 463 tests passed in 73.35 seconds.
- Extracted full-ZIP discovery suite: 463 tests passed in 73.49 seconds.
- Extracted full-ZIP selftest: passed in 0.37 seconds.
