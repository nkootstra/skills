---
name: triggering-none-10
tags: [triggering, none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the design skills
---
Write the API route that returns the list of invoices as JSON.
