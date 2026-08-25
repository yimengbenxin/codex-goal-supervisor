# Codex Goal Supervisor 3.1.4

Version: `3.1.4+codex.20260825153953`

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
- Startup allows a bounded five-second scheduling window under release-suite
  load. A child that still fails to publish bound-port metadata is terminated
  and its stale metadata is removed instead of being left behind.

## Truthful Native Goal Attestation

- A real first Goal creation is valid release evidence and no longer requires a
  no-value replacement ceremony.
- A true Goal replacement still requires durable replacement history and must
  not report the superseded objective as achieved.

## Leaner Release Verification

- The publisher still runs every verification test through both supported suite
  entry points across the release boundary: module mode against source and
  discover mode against the extracted full archive.
- It no longer executes both equivalent complete suites in both locations,
  removing two redundant full-suite passes while preserving source, archive,
  entry-point, selftest, and black-box release coverage.

## Non-blocking Feedback Authorization

- Explicit upload authorization still records consent and provisions the
  per-device credential during installation.
- Installation no longer synchronously flushes an existing feedback outbox;
  later events use the configured delivery path, and explicit flush remains
  available when requested.

These changes remove avoidable process tax without weakening real reuse
compatibility checks or active-ticket boundaries.
