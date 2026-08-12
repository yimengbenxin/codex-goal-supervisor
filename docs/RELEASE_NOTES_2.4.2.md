# Codex Goal Supervisor 2.4.2

This patch fixes two convergence gaps without adding a new workflow.

## Goal-wide Stall Recovery

- A manual, physical-device, login, or other external prerequisite is no
  longer allowed to silently become a global project blocker.
- When an unfinished confirmed Goal is about to stop for one such condition,
  the Stop hook forces one bounded review of the full Goal contract.
- The execution thread must defer the local prerequisite and continue the
  highest-value independent work, or prove that every remaining acceptance
  path is transitively blocked and report one exact human action.
- Codex's `stop_hook_active` flag prevents a continuation loop. Ordinary stops,
  certified completion, and responses already continuing independent work stay
  silent.

## Expert-assisted Goal Authoring

- A high-confidence industry-role match is now required input to new detailed
  Goal authoring, rather than an optional recommendation.
- A low-confidence domain match asks the user once to choose an eligible expert
  or skip it.
- A generic task with no relevant expert match stays silent.
- Expert input remains advisory; it cannot rewrite the confirmed North Star or
  replace the main thread as Goal author.

## Distribution Privacy

- `update-only` remains the recommended edition for devices that need automatic
  updates but must contain no feedback-upload client, endpoint, credential, or
  receiver code. Its public GitHub marketplace bundles the runtime and expert
  assets and contains no private feedback-server or asset-server endpoint.
- `offline` removes both feedback upload and automatic update code.
- `full` keeps optional feedback upload disabled until explicit project consent.

## Verification

- `python3 -m unittest -q verification.tests.test_goal_compass`: 455 tests
  passed in 85.31 seconds.
- `python3 -m unittest discover -s verification/tests -q`: 455 tests passed in
  84.92 seconds.
- `python3 assets/governor-harness/.agent/selftest/test_goal_compass.py`: passed
  in 0.38 seconds.
- Extracted-edition inspection confirmed that `update-only` contains the
  updater but no server directory, feedback configuration client, or feedback
  endpoint or private-server marker. `offline` also omits the updater.

Final archive hashes are published beside the immutable release assets rather
than embedded inside the archives they hash.
