---
name: triggering-readme-01
tags: [triggering, write-readme, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
Write a README for this repo.
