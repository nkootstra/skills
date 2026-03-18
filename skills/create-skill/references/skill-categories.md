# Skill Categories

Skills tend to cluster into recurring categories. The best skills fit cleanly into one; the more confusing ones straddle several. Use this taxonomy to help users identify what kind of skill they're building, and to check if their org is missing a category.

This isn't a definitive list, but it's a good framework for thinking about coverage.

---

## 1. Library & API Reference

Skills that explain how to correctly use a library, CLI, or SDK. These cover both internal libraries and common libraries that Claude sometimes gets wrong. They typically include a folder of reference code snippets and a list of gotchas for Claude to avoid.

**When to build one:** When Claude keeps making the same mistakes with a specific library, or when your internal tooling has undocumented conventions.

**What makes them good:** Focus on the information that pushes Claude out of its default behavior — gotchas, edge cases, and internal conventions. Don't restate what Claude already knows about the library from its training data.

**Examples:**
- `payments-sdk` — your internal payments wrapper: which methods require idempotency keys, which errors are retryable, how to handle webhook signature verification
- `infra-cli` — every subcommand of your internal deployment CLI with flags, required env vars, and examples of when to use each
- `design-tokens` — your design system's token names, spacing scale, and which components to prefer over raw HTML elements

**Typical structure:**
```
payments-sdk/
├── SKILL.md (overview, gotchas, routing table)
└── references/
    ├── api.md (method signatures and usage examples)
    ├── gotchas.md (common failure points)
    └── examples/ (code snippets organized by use case)
```

---

## 2. Product Verification

Skills that describe how to test or verify that code is working. These are often paired with an external tool like Playwright, tmux, or a headless browser for doing the verification.

Verification skills are extremely valuable for ensuring Claude's output is correct. It can be worth having an engineer spend a week making your verification skills excellent.

**When to build one:** When you need Claude to prove its work — not just write code, but confirm it actually works in a real environment.

**What makes them good:** Programmatic assertions on state at each step, not just "it looks right." Consider having Claude record a video of its output so you can see exactly what it tested. Include scripts in the skill for the deterministic parts of verification.

**Examples:**
- `checkout-e2e` — drives a headless browser through cart → checkout → payment, asserts database state and webhook delivery at each step
- `auth-flow-verifier` — tests signup, email verification, password reset, and session expiry with assertions on token state
- `cli-integration-tester` — runs CLI commands in a tmux session and asserts stdout/stderr patterns for tools that require a TTY

**Typical structure:**
```
checkout-e2e/
├── SKILL.md (workflow steps, assertion points, failure handling)
└── scripts/
    ├── run_flow.py (Playwright driver)
    ├── assert_state.py (database and webhook verification)
    └── record.sh (video recording wrapper)
```

---

## 3. Data Fetching & Analysis

Skills that connect to your data and monitoring stacks. These skills might include libraries to fetch data with credentials, specific dashboard IDs, and instructions on common workflows or ways to get data.

**When to build one:** When Claude needs access to internal data sources and the queries/schemas/credentials aren't obvious from the codebase alone.

**What makes them good:** Include composable helper functions that Claude can import and combine to build more complex analyses on the fly. Provide the canonical source-of-truth for common questions ("which table has the real user_id?").

**Examples:**
- `metrics-query` — which tables to join for revenue vs activations, where the canonical user_id lives, how to filter bot traffic
- `retention-analysis` — compute cohort retention curves, flag statistically significant drops, link to the segment definitions
- `grafana-lookup` — datasource UIDs, cluster names, and a symptom-to-dashboard lookup table

**Typical structure:**
```
metrics-query/
├── SKILL.md (common queries, table relationships, gotchas)
├── scripts/
│   ├── fetch_events.py (helper functions for warehouse queries)
│   └── compute_retention.py (cohort calculation logic)
└── references/
    └── schema.md (table definitions and relationships)
```

---

## 4. Business Process & Team Automation

Skills that automate repetitive workflows into one command. These are usually fairly simple instructions but might have dependencies on other skills or MCPs. For these skills, saving previous results in log files can help the model stay consistent and reflect on previous executions of the workflow.

**When to build one:** When someone on the team does the same multi-step process regularly and it's mostly mechanical.

**What makes them good:** Keep them simple. The value is in codifying the exact sequence so nothing gets skipped. Consider storing execution history so the skill can reference what happened last time (e.g., a standup skill that knows what changed since yesterday).

**Examples:**
- `daily-standup` — aggregates git activity, open PRs, and Linear tickets into a formatted standup; reads yesterday's post so it only shows what changed
- `new-ticket` — enforces your issue schema (required fields, valid enum values), then pings the right reviewer and links it in Slack
- `sprint-summary` — merged PRs, closed tickets, and deploy count → formatted team recap for the weekly sync

---

## 5. Code Scaffolding & Templates

Skills that generate framework boilerplate for a specific function in the codebase. Especially useful when your scaffolding has natural language requirements that can't be purely covered by code (e.g., "set up a new service with our auth, logging, and deploy config pre-wired").

**When to build one:** When new components/services/features always start from the same boilerplate, and that boilerplate involves decisions beyond what a code template can express.

**What makes them good:** Include template files in `assets/` that Claude can copy and customize. Combine deterministic scaffolding (file structure, config) with LLM-driven customization (naming, documentation, integration points).

**Examples:**
- `new-service` — scaffolds a new microservice with your auth middleware, structured logging, health check, and CI pipeline config pre-wired
- `new-db-migration` — generates a migration file, checks for common pitfalls (missing rollback, locking reads), and registers it in the migration runner
- `new-feature-flag` — creates the flag in your feature flag system, wires it into the codebase, and adds the cleanup checklist to the ticket

**Typical structure:**
```
new-service/
├── SKILL.md (steps, decisions to make, validation checklist)
├── assets/
│   ├── service-template/ (base project structure to copy)
│   └── config-template.yaml
└── scripts/
    └── scaffold.sh (file creation and registration)
```

---

## 6. Code Quality & Review

Skills that enforce code quality and help review code. These can include deterministic scripts or tools for maximum robustness. You may want to run these skills automatically as part of hooks or inside a GitHub Action.

**When to build one:** When Claude's default code review misses patterns specific to your codebase, or when you want consistent, repeatable quality checks.

**What makes them good:** Combine LLM judgment (understanding intent, catching logical errors) with deterministic scripts (style checking, pattern matching). Consider spawning a "fresh-eyes" subagent for adversarial review.

**Examples:**
- `pr-reviewer` — spawns a subagent that reviews without the author's context, files comments as GitHub review annotations, iterates until issues are addressed
- `security-audit` — checks for your org's known vulnerability patterns: hardcoded secrets, missing auth guards, unsafe deserialization
- `test-quality-check` — verifies tests actually assert behavior (not just that code runs), flags tests with no assertions or with `time.sleep`

---

## 7. CI/CD & Deployment

Skills that help you fetch, push, and deploy code. These skills may reference other skills to collect data.

**When to build one:** When your deployment process has org-specific steps that Claude can't infer from the codebase (approval flows, gradual rollouts, specific smoke tests).

**What makes them good:** Include guardrails for destructive operations. Make rollback procedures explicit. Reference monitoring dashboards to check after deployment.

**Examples:**
- `pr-shepherd` — watches a PR, re-triggers flaky checks, resolves merge conflicts when the base branch updates, and enables auto-merge once all checks pass
- `gradual-rollout` — builds, runs smoke tests, shifts 5% of traffic, monitors error rate for 10 minutes, promotes or rolls back automatically
- `hotfix-deploy` — creates an isolated branch from the release tag, cherry-picks the fix, runs the fast test suite, opens a PR with the incident linked

---

## 8. Runbooks

Skills that take a symptom (such as a Slack thread, alert, or error signature), walk through a multi-tool investigation, and produce a structured report.

**When to build one:** When incident response follows a repeatable pattern: same initial checks, same tools, same report format.

**What makes them good:** Map symptoms to investigation tools and query patterns. Produce structured output (not a wall of text) so the reader can quickly assess severity and next steps. Include links to relevant dashboards and log sources.

**Examples:**
- `api-latency-runbook` — maps high p99 to the usual suspects (slow queries, cache misses, upstream timeouts), runs the right queries, produces a findings report
- `alert-triage` — fetches the alert details, checks the standard indicators, summarizes findings and next steps in a structured format
- `request-tracer` — given a request ID, pulls matching spans and logs from every service that touched it, reconstructs the timeline

**Typical structure:**
```
api-latency-runbook/
├── SKILL.md (symptom routing, investigation steps, report template)
├── scripts/
│   ├── fetch_alert.py (pull alert details from your alerting system)
│   └── query_traces.py (multi-service span correlation)
└── references/
    └── dashboards.md (service → dashboard URL mapping)
```

---

## 9. Infrastructure Operations

Skills that perform routine maintenance and operational procedures — some of which involve destructive actions that benefit from guardrails.

**When to build one:** When operational procedures are well-defined but error-prone, especially when they involve destructive actions that need confirmation steps.

**What makes them good:** Include explicit guardrails for destructive operations (confirmation prompts, soak periods, Slack notifications before cleanup). Make the skill surface what it's about to do and wait for human confirmation on anything irreversible.

**Examples:**
- `stale-resource-cleanup` — identifies unused cloud resources, posts a summary to Slack, waits for human confirmation, then deletes with a dry-run first
- `cert-rotation` — rotates TLS certificates across services in the right order, verifies each before proceeding, rolls back if verification fails
- `cost-spike-investigation` — identifies which service or bucket caused a billing spike, traces it to the responsible team, and drafts the cost attribution report

---

## Choosing the Right Category

When helping a user identify which category their skill fits:

1. Ask what the skill should accomplish in one sentence
2. Match it to the closest category above
3. If it straddles two categories, consider whether it should be two skills or whether one category is clearly primary
4. Use the "typical structure" examples to guide the skill's file organization

If the user's need doesn't fit any category, that's fine — these are patterns, not requirements. But knowing the pattern helps write better skills because each category has different best practices (verification skills need assertions; data skills need composable helpers; runbooks need structured output).
