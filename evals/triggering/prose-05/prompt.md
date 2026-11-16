---
name: triggering-prose-05
tags: [triggering, write-prose, triggering-write-prose, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
My essay (drafts/essay.md) takes too long to get going; friends say the first half reads like a travel diary. Restructure it to start where it matters and cut the 'surprisingly, what I learned was' narration.
