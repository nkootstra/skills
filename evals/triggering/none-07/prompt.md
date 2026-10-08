---
name: triggering-none-07
tags: [triggering, none, near-miss, pilot]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the design skills
---
Change the primary button color to #0F766E.
