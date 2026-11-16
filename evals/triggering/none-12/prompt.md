---
name: triggering-none-12
tags: [triggering, none, triggering-none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
Why is my Next.js build failing with 'Module not found: Can't resolve @/lib/db'?
