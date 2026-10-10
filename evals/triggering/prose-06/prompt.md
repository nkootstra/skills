---
name: triggering-prose-06
tags: [triggering, write-prose, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
We shipped a migration tool. I need a short changelog piece explaining what changed and why it matters, no marketing adjectives, under 300 words. The internal spec is in docs/migration-spec.md.
