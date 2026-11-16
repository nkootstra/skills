---
name: triggering-code-01
tags: [triggering, improve-codebase, triggering-improve-codebase, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
This codebase has gotten messy over the last two years. Clean up the structure so it's easier to work in, without changing what it does.
