# Runbook Template

Use this template when building a skill that takes a symptom (alert, error, Slack thread) and walks through a structured investigation to produce a findings report. These skills codify your team's incident response patterns so that investigations are consistent and thorough.

## How to Customize

Replace everything in `[brackets]` with the user's specifics. Delete sections that don't apply.

---

## Template SKILL.md

```markdown
---
name: [name]-runbook
description: Investigates [type of issue] by walking through diagnostic steps and producing a structured findings report. Use when user mentions "[symptom 1]", "[symptom 2]", "[alert name]", "why is [thing] broken", "debug [system]", "investigate [issue]", or pastes an error/alert related to [domain]. Also trigger for "[service] is down", "something is wrong with [system]", or any incident triage related to [scope].
---

# [Issue Type] Runbook

## Purpose

Takes a symptom — an alert, error message, Slack thread, or user report — and walks through a structured investigation to determine root cause, severity, and next steps.

## Symptom Routing

Match the reported symptom to the right investigation path:

| Symptom | Likely cause | Start at |
|---------|-------------|----------|
| [e.g., "5xx errors spiking"] | [e.g., "Deployment regression or dependency failure"] | Step 1A |
| [e.g., "Latency above 2s"] | [e.g., "Database query degradation or cache miss storm"] | Step 1B |
| [e.g., "Queue depth growing"] | [e.g., "Consumer crash or processing bottleneck"] | Step 1C |
| Unknown / doesn't match above | General investigation | Step 1A |

## Investigation Steps

### Step 1A: [First investigation path, e.g., "Check recent deployments"]

- [e.g., "Query deploy log: when was the last deploy to this service?"]
- [e.g., "Compare error rate before and after the deploy"]
- [e.g., "Check the deploy diff for obvious issues"]

**Dashboard:** [e.g., "https://grafana.internal/d/service-health"]
**Log query:** [e.g., "`service=api level=error | json | count by status_code`"]

If this step reveals the cause → skip to Report. Otherwise → Step 2.

### Step 1B: [Alternative path, e.g., "Check database performance"]

- [e.g., "Query slow query log for the relevant time window"]
- [e.g., "Check connection pool utilization"]
- [e.g., "Look for lock contention"]

**Dashboard:** [e.g., "https://grafana.internal/d/database-health"]

If this step reveals the cause → skip to Report. Otherwise → Step 2.

### Step 2: [Deeper investigation, e.g., "Correlate across systems"]

- [e.g., "Given a request ID from the error, pull matching logs from every system that might have touched it"]
- [e.g., "Check if the issue correlates with traffic patterns"]
- [e.g., "Look for upstream dependency failures"]

### Step 3: [Escalation checks, e.g., "External dependencies"]

- [e.g., "Check third-party status pages (Stripe, AWS, etc.)"]
- [e.g., "Verify DNS resolution and certificate expiry"]

## Report Template

After investigation, produce a report in this format:

```
## Findings: [One-line summary]

**Severity:** [Critical / High / Medium / Low]
**Detected:** [timestamp]
**Investigated by:** [who ran the runbook]

### Summary
[2-3 sentences describing what happened and why]

### Timeline
- [timestamp] — [event]
- [timestamp] — [event]

### Root Cause
[Detailed explanation of the root cause]

### Impact
- [e.g., "~500 users saw 500 errors over a 12-minute window"]
- [e.g., "No data loss confirmed"]

### Resolution
- [What was done to fix it, or what needs to be done]

### Follow-up Actions
- [ ] [e.g., "Add circuit breaker to prevent cascade"]
- [ ] [e.g., "Add monitoring for this specific failure mode"]
- [ ] [e.g., "Update runbook with this new symptom pattern"]
```

## Gotchas

- [e.g., "Grafana dashboards use UTC — convert timestamps before comparing with local logs"]
- [e.g., "The log query tool has a 10k result limit — use time windows to narrow results"]
- [e.g., "Some services log to a different cluster — check both us-east-1 and eu-west-1"]
- [e.g., "If the alert is for a canary deploy, check canary-specific dashboards first"]
```

---

## Customization Checklist

When filling in this template, make sure you've captured:

- [ ] Symptom routing table (symptom → likely cause → where to start)
- [ ] Investigation steps with specific queries, dashboards, and commands
- [ ] Dashboard URLs and log query patterns for each step
- [ ] Clear decision points (when to continue vs skip to report)
- [ ] Report template with all required sections
- [ ] Severity classification criteria
- [ ] Gotchas (timezone issues, tool limitations, multi-region quirks)
- [ ] Scripts in `scripts/` for automated data fetching (alert details, log queries)
- [ ] References in `references/` for service-to-dashboard mappings
