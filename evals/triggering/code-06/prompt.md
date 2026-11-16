---
name: triggering-code-06
tags: [triggering, improve-codebase, triggering-improve-codebase, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
The src/orders module is full of circular imports and copy-pasted logic. Restructure it.
