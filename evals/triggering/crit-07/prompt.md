---
name: triggering-crit-07
tags: [triggering, design-critique, triggering-design-critique, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-critique
---
Do a heuristic evaluation of the signup form in src/components/SignupForm.tsx.
