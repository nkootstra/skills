---
name: triggering-readme-06
tags: [triggering, write-readme, triggering-write-readme, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-readme
---
This is a pnpm monorepo with four packages and no top-level docs. What should someone see when they open the repo on GitHub? Write it.
