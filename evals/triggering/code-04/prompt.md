---
name: triggering-code-04
tags: [triggering, improve-codebase, triggering-improve-codebase, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
Do a code quality audit of this repo and tell me what to refactor first. Don't change anything yet.
