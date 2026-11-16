---
name: triggering-readme-08
tags: [triggering, write-readme, triggering-write-readme, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
Generate the docs for this library in the README: install, usage and an API overview.
