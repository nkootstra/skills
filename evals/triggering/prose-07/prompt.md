---
name: triggering-prose-07
tags: [triggering, write-prose, triggering-write-prose, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
Write a commit message for the changes I just made. They fix a race in background sync.
