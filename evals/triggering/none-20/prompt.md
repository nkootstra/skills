---
name: triggering-none-20
tags: [triggering, none, triggering-none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
Extract the date parsing inside parseDate in src/utils/format.ts into its own helper function.
