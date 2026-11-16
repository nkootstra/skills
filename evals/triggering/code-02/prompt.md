---
name: triggering-code-02
tags: [triggering, improve-codebase, triggering-improve-codebase, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads improve-codebase
---
Every time we add a payment method we end up touching nine files across four folders. Sort out the structure so that stops happening.
