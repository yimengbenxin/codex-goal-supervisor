# Codex Goal Supervisor 2.8.8

## Candidate scope

- Keep the existing Goal, observer, optional ticket, company-role, Auditor, and
  mark-only Janitor behavior unchanged.
- Add one domain-neutral route-convergence rule without adding a command or a
  mandatory workflow.

## Route convergence

- Every active technical route is anchored to the detailed Goal's source
  requirements, first principles, and final acceptance.
- One route failure stays silent. Two same-cause failures separated by 30
  minutes, or three immediate failures without new Goal evidence, produce one
  structured route reassessment.
- Reassessment requires current online research, comparison of at least two
  materially different routes, and execution of the smallest route that can
  satisfy the same acceptance.
- Parameter-only retries retain the same route history. A materially different
  route remains available.
- Only another exact retry of the proven failed action can reach a targeted
  rail, and only after the sparse Judge confirms it at high confidence.
- Persisted incident state contains bounded hashes and cause families, never
  raw commands, tool output, source text, credentials, or network addresses.
- Project hooks tolerate hosts that omit the explicit event phase when a real
  result envelope is present, and accept common result field wrappers.

## Verification

- Added cross-domain route incidents for software, CAD, data, mobile,
  manufacturing, robotics, finance, and simulation fixtures.
- Added a direct installed-project hook regression for omitted event phases,
  alternate result wrappers, and exit-code spelling.
- Source suites and the fixed Luna Max blackbox must pass before publication.

## Release boundary

Publication requires the exact clean 2.8.8 commit to pass the fixed Luna Max
blackbox task before source, extracted-package, edition, checksum, and remote
marketplace verification may write to the release channels.
