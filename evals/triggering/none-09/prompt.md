---
name: triggering-none-09
tags: [triggering, none, triggering-none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
What's the CSS property for making text not wrap?
