# Codex Goal Supervisor 2.4.3

This patch keeps a long-running Goal current without turning ordinary user
messages into a new governance flow.

## Durable Direction Confirmation

- A temporary request, question, implementation detail, sequencing change,
  short task, and a subgoal already contained by the confirmed Goal stay
  silent.
- A non-explicit direction change is surfaced only after the sparse read-only
  Judge reports a high-confidence durable change outside both the concise North
  Star and detailed Goal contract.
- One Goal generation and session can have only one pending confirmation, so
  rewording the same direction does not produce repeated prompts.
- The plugin never rewrites the North Star automatically. When the user
  confirms, the execution thread must rebuild the concise North Star and the
  detailed Goal contract together. A declined change preserves both.

## Verification

- `python3 -m unittest -q verification.tests.test_goal_compass`: 461 tests
  passed in 84.08 seconds.
- `python3 -m unittest discover -s verification/tests -q`: 461 tests passed in
  82.78 seconds.
- `python3 assets/governor-harness/.agent/selftest/test_goal_compass.py`: passed
  in 0.38 seconds.
