---
name: triggering-none-18
tags: [triggering, none, near-miss]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads none of the skills
---
Generate an OpenAPI spec for the routes in src/api.
