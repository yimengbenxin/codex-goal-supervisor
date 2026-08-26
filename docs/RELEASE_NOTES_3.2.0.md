# Codex Supervisor 3.2.0

Version: `3.2.0+codex.20260826152106`

## Optional Reproducible Agent Assembly

- Adds an on-demand Agent Assembler for packaging an already working business
  loop as a portable Agent.
- Uses an explicit blueprint for entry points, inputs, outputs, consumers,
  capabilities, declared package paths, and machine acceptance.
- Fetches selected capabilities into an isolated project-local cache instead of
  copying community projects into the plugin or product source.
- Verifies the real business loop before locking exact capability revisions and
  tree hashes.
- Produces a deterministic ZIP containing only declared product, capability, and
  assembly metadata paths.
- Records adopted or rejected capability experience as local metadata only.
  Source and attachments are excluded, and no sharing occurs without the
  separate consent-gated bridge available only in the full edition.

## Product Identity

- The public display name is now Codex Supervisor.
- The package slug remains `codex-goal-supervisor` so existing installations and
  update channels continue to resolve the same plugin.
- General and Goal Profiles continue to use the same capability core. Agent
  assembly is optional in both profiles and does not impose tickets, receipts,
  or packaging work on ordinary tasks.

## Verification

- Deterministic Agent Assembler tests cover blueprint validation, isolated
  fetching, verification, locking, deterministic packaging, path exclusion,
  metadata-only experience, and release-edition separation.
- A real Luna Max black-box run in a fresh project created and exactly synchronized
  a 3,500-character Goal, fetched a pinned MIT text-normalizer capability, built a
  portable support Agent, extracted it in a clean directory, and returned
  `category=billing` with `normalizer_source=packaged-capability`.
- The clean candidate worktree retained the same content fingerprint from start
  to finish, and the packaged ZIP excluded `.agent`, `.codex`, `.git`, feedback,
  credentials, and undeclared paths.

This release adds a reusable engineering tool without changing Codex Supervisor's
supreme rule: every action and every supervisory intervention must produce net
execution benefit.
