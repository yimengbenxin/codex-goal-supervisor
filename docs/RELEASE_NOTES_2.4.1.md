# Codex Goal Supervisor 2.4.1

This patch makes scheduled GitHub marketplace updates honor the device's
operating-system HTTP/HTTPS proxy when no proxy environment variable is set.
An explicit process proxy remains authoritative. No device-specific proxy
address is bundled, and project activation or feedback consent is unchanged.

The fix was prompted by a clean-install regression where the public GitHub
marketplace was correct but Git smart HTTP bypassed the active macOS system
proxy and timed out. Isolated full and update-only installs succeeded after the
same proxy was inherited.

## Verification

- `python3 -m unittest -q verification.tests.test_goal_compass`: 448 tests
  passed in 87.099 seconds.
- `python3 -m unittest discover -s verification/tests -q`: 448 tests passed in
  85.289 seconds.
- `python3 assets/governor-harness/.agent/selftest/test_goal_compass.py`: passed
  in 0.32 seconds.

## Release Artifacts

```text
db6f8d43908a0dd6834897648650969278abc98a464986ea006c4f5a64286574  codex-goal-supervisor-2.4.1+codex.20260812042244-offline.zip
3398666eeb6c656b918ecae3d4bd9f79fcdafafbcae127a7a6311d5b9379f833  codex-goal-supervisor-2.4.1+codex.20260812042244-update-only.zip
a3ece21a59a479fff2d2230101da9e1ebc9ee86cf1505a8c2d2d52ed197da8dc  codex-goal-supervisor-2.4.1+codex.20260812042244-full.zip
```
