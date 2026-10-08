---
name: triggering-none-01
tags: [triggering, none, near-miss, pilot]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the design skills
---
Fix the TypeError in src/components/InvoiceTable.tsx: 'Cannot read properties of undefined (reading map)'.
