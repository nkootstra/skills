---
name: triggering-prose-01
tags: [triggering, write-prose, direct]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
I wrote this messy draft on our code-review process (notes/code-review.md) and want it turned into a proper blog post. Keep my voice as a working engineer and don't invent things I didn't say.
