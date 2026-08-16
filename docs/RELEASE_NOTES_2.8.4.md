# Codex Goal Supervisor 2.8.4

## Candidate scope

- Preserve the 2.5-current verified business surface.
- Keep one concise confirmed North Star while projecting one independently
  useful 2-24 hour phase into native Goal mode.
- Make the structured phase input directly consumable instead of requiring an
  execution Agent to infer JSON nesting from repeated validation failures.

## Contract usability fix

- The installed README now contains the canonical outline and phase JSON shape.
- The Skill states that `goal_definition` is a complete structured object and
  that no preparatory detailed `goal-set` is required.
- `phase-set` and `phase-advance` return the installed contract reference when
  validation fails.
- Common unambiguous aliases are normalized for compatibility, including
  `detailed_goal_definition`, `validation_catalog_ids`, `id`,
  `timebox_hours`, and `depends_on`.

## Release boundary

This is a local candidate. It is not published until source, extracted-package,
edition-boundary, selftest, and fixed Luna Max blackbox verification pass.
