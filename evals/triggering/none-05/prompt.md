---
name: triggering-none-05
tags: [triggering, none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the design skills
---
Rename the Button component's 'kind' prop to 'variant' everywhere.
