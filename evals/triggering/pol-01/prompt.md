---
name: triggering-pol-01
tags: [triggering, interface-polish, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
Polish the settings page so it feels premium. src/pages/Settings.tsx
