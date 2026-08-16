# Codex Goal Supervisor 2.8.6

## Candidate scope

- Preserve the verified 2.5-current business surface and the structured phased
  Goal contract introduced in 2.8.3-2.8.5.
- Close only the integration gaps exposed by the fixed Luna Max blackbox.

## Blackbox-driven fixes

- The installed lightweight project hook now records the first real product
  write and successful validation for an ACTIVE structured phase even when no
  optional ticket is ACTIVE.
- A successful `phase-complete` records its authoritative catalog validation as
  first valid evidence when no earlier hook evidence exists, without inventing
  a product action.
- Convergence segments now recognize completed program phase IDs as satisfied
  dependencies while preserving blockers for unknown dependencies.
- Hook dispatch from the bundled `assets/governor-harness` template stops at
  the template boundary instead of falling back to an observed source checkout.

## Release boundary

This remains a local candidate. It is not published until source,
extracted-package, edition-boundary, selftest, and fixed Luna Max blackbox
verification pass.
