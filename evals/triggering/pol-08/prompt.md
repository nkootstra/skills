---
name: triggering-pol-08
tags: [triggering, interface-polish, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
Clean up the dark mode on the marketing page, the cards look washed out and the screenshots glow. src/pages/Home.tsx
