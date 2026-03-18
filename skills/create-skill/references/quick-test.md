# Quick Test (Claude.ai)

> **Environment:** This reference applies to Claude.ai only. If you're in Claude Code or Cowork (with subagents), read `references/full-eval.md` instead for the full parallel eval workflow.

Claude.ai doesn't have subagents, so some mechanics change. Here's the adapted workflow:

## Running Test Cases

No parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — the human review step compensates. Skip baseline runs.

## Reviewing Results

If you can't open a browser (e.g., Claude.ai's VM has no display), skip the browser reviewer. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file (.docx, .xlsx, etc.), save it and tell the user where to download it. Ask for feedback inline: "How does this look? Anything you'd change?"

## Benchmarking

Skip quantitative benchmarking — it relies on baseline comparisons that aren't meaningful without subagents. Focus on qualitative feedback.

## The Iteration Loop

Same as always — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem.
