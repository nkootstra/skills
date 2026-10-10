---
name: triggering-readme-03
tags: [triggering, write-readme, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
Document how to run this project locally, starting from a fresh clone.
