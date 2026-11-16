---
name: triggering-code-03
tags: [triggering, improve-codebase, triggering-improve-codebase, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
We want to pay down tech debt in the services/ package this sprint. Find what's worth fixing and fix it.
