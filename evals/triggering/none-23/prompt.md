---
name: triggering-none-23
tags: [triggering, none, triggering-none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
Run the linter and fix all the formatting errors it reports.
