---
name: triggering-crit-08
tags: [triggering, design-critique, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-critique
---
My designer friend said the header 'has no hierarchy'. Is she right? What does that even mean here? src/components/Header.tsx
