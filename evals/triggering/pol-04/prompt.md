---
name: triggering-pol-04
tags: [triggering, interface-polish, triggering-interface-polish, indirect]
runs: 2
plugins: ["../../.."]
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Loads interface-polish
---
Add proper loading, empty and error states to the invoices table in src/components/InvoiceTable.tsx.
