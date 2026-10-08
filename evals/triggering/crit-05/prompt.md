---
name: triggering-crit-05
tags: [triggering, design-critique, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-critique
---
We keep saying our app should feel 'calm and trustworthy'. Can you score the current UI against that and tell me where it falls short?
