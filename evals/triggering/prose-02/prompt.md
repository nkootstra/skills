---
name: triggering-prose-02
tags: [triggering, write-prose, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads write-prose
---
Our about page (content/about.md) reads like an AI wrote it. Full of 'seamless', 'revolutionary', 'passionate team'. Rewrite it so it sounds like an actual person with a point of view, keeping the facts.
