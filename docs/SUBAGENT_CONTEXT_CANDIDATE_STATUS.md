# Subagent Context Candidate Status

Scope: supported Hook-based result contracts; not universal transport filtering.

## Implemented

- Project-local SubagentStart supplies a compact result contract.
- SubagentStop validates the child final shape and bounded character length,
  requesting a limited correction when needed.
- Result metadata separates worker execution, worker-reported validation, and
  root acceptance. Receiving DONE does not grant acceptance.
- Task revisions record supersession. Duplicate delivery preserves acceptance;
  changed same-revision output and late old revisions cannot replace the current
  result. Supersession alone does not invent a parent rework decision.
- Full logs and invalid finals remain local. Status details are opt-in.

## Unmet Requirements

- The plugin has not demonstrated transport-level replacement of every child
  payload before parent model input. Hook correction is not equivalent to that
  guarantee. In particular, retry exhaustion and hook failure can leave the
  original worker result available through the host.
- The current bound is characters, not the MRD's exact 250 model-token limit.
- Revision metadata is recorded on completion; dispatch-time parent-owned
  allocation and a root acceptance update interface are not implemented.
- Worker validation text has explicit worker_report / UNVERIFIED provenance;
  independent command-to-result attestation is not implemented.
- Twenty concurrent synthetic hook results pass local tests. This is not proof
  of twenty real model workers or of parent model-input coverage.
- Native delayed notification and interrupted-worker paths still need a real
  integration test. A child final visible in a UI is insufficient evidence.

## Validation

The latest source run passed 629 tests across 39 modules in 43.187 seconds.
New regression cases cover duplicate completion, changed same-revision output,
and late old-revision delivery, plus missing-Hook repair, first-install Hook
generation, active-state preservation and repeat-ensure idempotence. Selftest
passed.

The initial preflight conclusion that Luna was unavailable was incomplete.
After configuring `agents.default_subagent_model = "gpt-5.6-luna"` and
`agents.default_subagent_reasoning_effort = "max"`, real parent and child
turn_context records confirmed Luna/max. The fixed test task exercised real
native children and independently reran four passing business tests.

The earlier diagnostic failed because the project configuration layer was
disabled by trust checks; a CLI trust override did not enable discovery. After
persisting exact project trust and trusting the reviewed Hook hashes, native
hooks/list reported all nine project hooks trusted. Tool observations and real
SubagentStart/SubagentStop registry writes then occurred.

The fixed test task's final native children both have Luna/max turn_context
records. The business worker ran four passing tests and returned 117 characters;
the worker asked for a 5000-character non-structured final instead followed the
startup contract and returned 145 characters. Both were registered as DONE with
UNREVIEWED acceptance. This verifies the supported startup contract and terminal
recording path, not universal transport replacement. No Stop correction retry
was exercised by these compliant child results.

One intermediate diagnostic incorrectly launched a root CLI instead of a
native child and is excluded from acceptance. Its missing Subagent events are
not evidence of a plugin failure. Runtime Hook integration is now demonstrated;
the broader unmet MRD guarantees above remain open.

The prematurely installed personal candidate was removed to avoid simultaneous
3.2.0 and 3.3.0 activation. Source changes remain available locally; the stable
release is retained until the verified update is installed. This version must
not be represented as full MRD acceptance: the unmet guarantees above remain
outside its verified scope.
