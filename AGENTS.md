# Goal Supervisor Project Requirements

## Real Black-Box Validation

- Every Goal Supervisor release or business-capability change must be validated through a real Codex task in addition to deterministic tests.
- Use the Codex task titled `插件专用测试线程`, thread ID `01a00666-8821-7461-a9ab-113205b3bdd0`, for the real black-box run.
- Run the black-box task with Luna Max and require it to load the currently installed Goal Supervisor plugin and complete a real product goal.
- Require the task to complete required online reuse research, run plugin `goal-set --require-detailed`, and only then activate Codex's native Goal mode with the exact returned `goal_mode_objective`. Plugin state is not a substitute for native Goal mode, and an early native Goal created from the rough prompt is not valid evidence.
- Compare the native `get_goal` objective byte-for-byte with the plugin `goal_mode_objective`; length and SHA-256 must match before implementation.
- Require an actual online reuse-research tool call before the detailed project Goal is finalized; local package inspection alone is not research evidence.
- Do not replace this evidence with unit tests, verification fixtures, the implementation thread's self-assessment, or a subagent simulation.
- Do not coach the black-box task with expected internal behavior or test answers. Give it the product goal, require plugin use, and observe its actual behavior.
- Use a fresh isolated project directory for every black-box scenario so repository state and product artifacts do not leak between runs.
- A release is not complete until deterministic regression, extracted-package verification, and this real-task black-box validation all pass or any remaining failure is reported explicitly.
- Publication is strictly last: the exact clean candidate commit must pass the real Luna Max black box and independent product acceptance before any repository, marketplace, release, or update channel is written.
