---
name: triggering-pol-03
tags: [triggering, interface-polish, triggering-interface-polish, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
The app works but looks like a hackathon project. Make the team members list in src/components/TeamList.tsx not look generic.
