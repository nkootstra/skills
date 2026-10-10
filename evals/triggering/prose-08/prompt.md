---
name: triggering-prose-08
tags: [triggering, write-prose, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
Draft the PR description for this branch using our template in .github/pull_request_template.md. Unit tests passed; browser testing was not run.
