---
name: triggering-prot-07
tags: [triggering, intentional-prototyping, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads intentional-prototyping
---
Show me 12 random variations of this tooltip's entrance animation in a grid so I can pick one.
