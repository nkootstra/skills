---
name: triggering-readme-05
tags: [triggering, write-readme, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
I renamed the npm scripts last week: dev is now start:dev and test is now test:unit. Make sure the docs keep up.
