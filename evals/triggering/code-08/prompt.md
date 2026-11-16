---
name: triggering-code-08
tags: [triggering, improve-codebase, triggering-improve-codebase, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
Refactor the whole backend for maintainability. Behavior has to stay exactly the same.
