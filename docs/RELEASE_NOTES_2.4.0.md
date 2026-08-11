# Codex Goal Supervisor 2.4.0

This release improves convergence without making ordinary work more procedural.

## Goal Authoring

- `agency_role_pack.py goal-brief` can prepare one task-specific industry-expert
  input contract when an explicit lookup has a high-confidence match.
- Weak matches produce `NO_HIGH_CONFIDENCE_ROLE`; zero expert input remains valid.
- Experts provide domain modules, dependencies, acceptance evidence, failure
  modes, reusable tools, and user-facing questions. They cannot rewrite the
  user's words, confirmed North Star, scope, acceptance, or main-thread authority.

## Collaboration Liveness

- Cross-thread agreement, praise, and restatement no longer count as progress.
- A first evidence-free handoff warns. Two consecutive evidence-free handoffs
  produce `CONSENSUS_WITHOUT_PROGRESS` and require execution, validation, or one
  concrete escalation.
- New evidence, artifact references, or accepted state transitions reset the
  collaboration counter.

## Sanitized Feedback Archive

- Client behavior remains unchanged: feedback is local by default and remote
  delivery requires explicit project consent.
- The receiver can optionally mirror already-validated sanitized metadata in
  bounded batches to a dedicated private GitHub repository.
- GitHub write credentials stay on the server. Mirror failure preserves SQLite
  events and never blocks project work.

## Verification

- Added role selection tests for packaging, healthcare, weak matches, and
  explicit selection.
- Added collaboration liveness tests for empty consensus and evidence recovery.
- Added server-side GitHub mirror success, retry, and client-credential-boundary
  tests.
- `python3 -m unittest -q verification.tests.test_goal_compass`: 446 tests
  passed in 83.111 seconds.
- `python3 -m unittest discover -s verification/tests -q`: 446 tests passed in
  83.211 seconds.
- `python3 assets/governor-harness/.agent/selftest/test_goal_compass.py`: passed.

## Release Artifacts

```text
40f5206001403ef4241f837f4d87f997bee7b8ee069b9e4652e05fa0e9e60a6b  codex-goal-supervisor-2.4.0+codex.20260812025957-offline.zip
f68facf29800193355e53a040acb414d4912c44dccc3bfdda0103ebfc5461867  codex-goal-supervisor-2.4.0+codex.20260812025957-update-only.zip
15ede86c13b314de48e75c3b215375e1da2099c992d7212701e7cc13cddd37ce  codex-goal-supervisor-2.4.0+codex.20260812025957-full.zip
```
