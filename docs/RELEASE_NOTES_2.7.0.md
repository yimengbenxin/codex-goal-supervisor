# Codex Goal Supervisor 2.7.0

This release makes the detailed Goal route visible without introducing another
project state or forcing ordinary work through a diagram workflow.

## Live technical route

- Every newly authored or materially rewritten detailed Goal keeps its complete
  high-level technical route in the existing Goal contract before product work
  starts: nodes, dependencies, actions, inputs, outputs, consumers, impact,
  exit criteria, timeboxes, and final acceptance.
- `goal-set --require-detailed` starts or reuses a project-local dashboard and
  returns its loopback URL.
- The dashboard reads the authoritative North Star and convergence files and
  refreshes every two seconds. Segment start and completion are visible without
  manual page reloads.
- Large nodes can be opened to inspect actions, input/output flow, downstream
  consumers, affected paths or modules, acceptance, and deadlines.
- Subnodes are optional and appear only when the user asks for deeper detail or
  a node is too broad to execute safely.
- Ordinary one-off Goals and tasks do not start the dashboard or gain a route
  ceremony.

## Runtime boundary

- The server binds only to `127.0.0.1`, uses no external page assets, and cannot
  modify project state.
- `roadmap --snapshot` exposes the bounded JSON projection; `roadmap --stop`
  closes the local service.
- Dashboard failure is fail-open for product work because visualization is not
  authority-bearing evidence.
- Remote runtime verification now rejects a package missing either the roadmap
  service or its HTML surface.

## Verification

- Route-contract enforcement, optional subnodes, node-state transitions,
  loopback binding, live refresh data, offline HTML, low-noise status, and
  installer completeness are covered by regression tests.
- Source, discovery, selftest, and extracted-release verification run before
  publishing.
