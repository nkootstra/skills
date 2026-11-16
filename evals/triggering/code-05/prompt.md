---
name: triggering-code-05
tags: [triggering, improve-codebase, triggering-improve-codebase, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
Our coding agents keep getting lost in this repo and breaking unrelated things. Make it easier for them to work in.
