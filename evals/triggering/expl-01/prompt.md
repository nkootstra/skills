---
name: triggering-expl-01
tags: [triggering, design-exploration, triggering-design-exploration, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-exploration
---
Give me a few genuinely different design directions for an empty state on the projects page.
