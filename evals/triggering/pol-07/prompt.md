---
name: triggering-pol-07
tags: [triggering, interface-polish, hard]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
Make the modal in src/components/Modal.tsx feel right: how it opens, closes, focus, escape, all the details.
