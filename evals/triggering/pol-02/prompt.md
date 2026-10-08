---
name: triggering-pol-02
tags: [triggering, interface-polish, indirect, pilot]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
We're launching Monday. Go through src/pages/Dashboard.tsx and make it feel finished: empty states, loading, errors, all of it.
