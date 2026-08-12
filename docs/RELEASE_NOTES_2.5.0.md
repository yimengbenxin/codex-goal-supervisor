# Codex Goal Supervisor 2.5.0

This release makes verified local releases converge automatically with every
public distribution channel.

## Verified Publishing

- `scripts/publish_verified_release.py` is now the single maintainer release
  command.
- It refuses a dirty or uncommitted source tree.
- It compiles and verifies source, builds all three physical editions, and
  reruns module, discovery, and selftest verification from the extracted full
  ZIP.
- It pushes the canonical source, creates the GitHub Release with all ZIPs and
  a SHA-256 manifest, then updates the full and update-only marketplaces.
- It clones both online marketplaces again and verifies the exact version and
  edition before reporting success.
- Publishing is idempotent. An existing matching release is accepted; a
  conflicting asset set is refused.

## Verification

- Source module suite: 470 tests passed.
- Source discovery suite: 470 tests passed.
- Selftest: passed in under one second.
- The publisher repeats both full suites and selftest from the extracted full
  release archive before any online write.

## Distribution Boundary

- The offline edition contains neither updater, feedback transport, nor release
  publisher code.
- The update-only edition contains the client updater but no feedback transport
  or release publisher code.
- The full edition retains the maintainer publisher. Project feedback upload
  remains disabled until explicit project consent.

## Goal Direction Fixes

- Durable North Star change confirmation survives session changes and context
  compaction without repeated prompts.
- A question that mentions North Star confirmation cannot be mistaken for the
  user's confirmation.
