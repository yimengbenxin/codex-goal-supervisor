# Codex Goal Supervisor 2.6.0

This release keeps long Codex work anchored to reusable implementation routes
and real delivery time without turning either into a ticket ceremony.

## Goal-authored reuse

- Every detailed Goal records a completed tool and article investigation before
  implementation begins.
- The Goal body carries the actionable reuse decision for each affected module,
  including integration and validation, instead of storing only a research log.
- Continuing long tasks refresh existing tools, versions, and remaining-action
  fit after 24 hours. The refresh is project-scoped and does not repeat on every
  conversation continuation.
- A reusable candidate requires visible user confirmation of reuse choice and
  commercial context before the final technical plan is accepted.

## Real segment deadlines

- Every capability segment has an hour-level target and a bounded reminder
  cadence in the detailed Goal contract.
- The first product write silently starts the only unambiguous dependency-ready
  segment and records an absolute wall-clock deadline.
- Ambiguous parallel segments are not guessed; the execution Agent can select
  one explicitly with `convergence --start-segment`.
- Segments of two hours or less normally have no pre-deadline interruption.
  Longer segments receive bounded checkpoints, including a guaranteed deadline
  checkpoint, until evidence-backed completion clears the reminder.
- Hooks can report a due checkpoint on the next Codex event, but do not claim to
  wake a completely idle Codex client.

## Low-noise boundary

- Ordinary project writes remain silent.
- Automatic segment start requires a unique eligible segment or an exact
  structured action match.
- The 24-hour reuse reminder requires a confirmed detailed Goal and a prior
  expired probe, and is emitted once per probe cycle.
- Tickets, company roles, Custodian, Auditor, and Janitor remain optional tools.

## Verification

- Source module suite: 481 tests passed.
- Source discovery suite: 481 tests passed.
- Selftest: passed in under one second.
- The verified publisher repeats both suites and selftest from the extracted
  full release archive before publishing any release asset.
