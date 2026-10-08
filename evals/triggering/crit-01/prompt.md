---
name: triggering-crit-01
tags: [triggering, design-critique, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-critique
---
Can you critique the settings page in src/pages/Settings.tsx? Be specific.
