# Codex Goal Supervisor 3.1.2

Version: `3.1.2+codex.20260825115629`

## Conditional Commercial-Use Consultation

- A reusable candidate still requires a visible use, adapt, or reject choice.
- Commercial or non-commercial status is requested only when it changes license
  compatibility, pricing, permitted use, or the integration boundary.
- Permissive and otherwise confirmed-compatible reuse routes no longer block a
  detailed Goal merely because commercial status was not collected.
- Clearly restricted, separately licensed, or unknown-license candidates retain
  the commercial-use question before the route is finalized.
- Goal-definition errors distinguish adoption consultation from commercial
  compatibility consultation so the next action asks only the necessary question.

## Faster Active-Project Hook Dispatch

- An ACTIVE project now delegates to the full ticket contract hook in the same
  Python process instead of starting a second interpreter.
- The change preserves fail-open observer behavior and ticket enforcement while
  removing the duplicated startup that could exceed the hook time budget under
  full-suite or machine load.

## Stable Roadmap Startup Witness

- The live roadmap starts with an isolated standard-library Python process.
- Successful loopback binding plus atomic server metadata is the startup
  witness; a delayed second HTTP scheduling round no longer mislabels an
  already-bound service as `START_FAILED`.

## Truthful Native Goal Attestation

- A real first Goal creation is valid release evidence and no longer requires a
  no-value replacement ceremony.
- A true Goal replacement still requires durable replacement history and must
  not report the superseded objective as achieved.

These changes remove avoidable process tax without weakening real reuse
compatibility checks or active-ticket boundaries.
