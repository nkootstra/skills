---
name: triggering-none-02
tags: [triggering, none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the design skills
---
Convert #4F46E5 to HSL and OKLCH.
