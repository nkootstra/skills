---
name: triggering-none-06
tags: [triggering, none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
Add a unit test for the formatCurrency util in src/utils/format.ts.
