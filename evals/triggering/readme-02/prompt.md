---
name: triggering-readme-02
tags: [triggering, write-readme, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
Our setup docs are out of date. Fix them so they match what the project actually does now.
