---
name: triggering-crit-06
tags: [triggering, design-critique, hard, pilot]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads design-critique
---
Is the checkout flow in src/pages/Checkout.tsx good enough to ship, visually? Just give me your assessment, don't change anything.
