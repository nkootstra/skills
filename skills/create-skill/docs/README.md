# create-skill

A skill that helps you create, improve, and manage other skills. It works for everyone — developers, designers, writers, anyone who wants Claude to work the way they do without re-explaining every time.

## Installation

```bash
npx skills add nkootstra/skills --skill create-skill
```

## What's Included

```
create-skill/
├── SKILL.md                              # Core skill (wizard, 4 creation paths, writing guide)
├── evals.json                            # 18 test cases
├── references/
│   ├── skill-categories.md               # 9 skill categories with examples
│   ├── advanced-patterns.md              # Config, memory, hooks, composable scripts
│   ├── claude-md-guide.md                # When to fix CLAUDE.md / AGENTS.md instead of making a skill
│   ├── full-eval.md                      # Formal eval workflow (Claude Code / Cowork)
│   ├── quick-test.md                     # Simplified testing (Claude.ai)
│   ├── description-optimization.md       # Automated trigger optimization
│   └── schemas.md                        # JSON schemas for evals, grading, benchmarks
└── templates/
    ├── content-writer.md                 # Blog posts, newsletters, consistent voice
    ├── document-generator.md             # Reports, proposals, structured docs
    ├── verification.md                   # End-to-end testing with assertions
    ├── scaffolding.md                    # Code boilerplate generation
    └── runbook.md                        # Incident investigation workflows
```

## Demo Prompts

Copy-paste any of these to see the skill in action.

### Create a skill from scratch

Simple request — generates a minimal skill immediately:
> I write a weekly newsletter about AI. Every time I start a new issue I have to re-explain my voice and format. Can you make a skill for it? I like short punchy sentences, no fluff, and I always end with a "one thing to try this week" section.

Vague request — the wizard draws out specifics before generating:
> I keep repeating myself with Claude when setting up new client projects. Can you help me automate that somehow?

Complex request with scripts — separates deterministic tasks from LLM tasks:
> Build me a skill for processing bank statement PDFs. Extract transactions, categorize them, calculate monthly totals per category, and flag any transaction that's 3x the average for its category. Bundle whatever scripts make sense.

### Start from a template

Browse what's available:
> What kinds of skills can I make? Do you have any templates?

Verification skill — end-to-end testing with assertions:
> I need a skill that verifies our checkout flow works after every deploy. It should drive a headless browser through cart → checkout → payment with Stripe test cards, assert the order state in our database, and save screenshots at each step.

Runbook — incident investigation:
> Our payments service goes down once a month and it's always the same investigation. Can you make a runbook skill that walks through the checks and produces a structured findings report?

Scaffolding — code boilerplate:
> Make a skill that scaffolds a new microservice in our monorepo with our standard auth, logging, and deploy config pre-wired.

### Turn a conversation into a skill

After working through any process with Claude:
> Turn this into a skill

### Review and fix an existing skill

Diagnose problems with a skill you already have:
> Review my skill and tell me what's wrong. It works OK but sometimes the output is inconsistent.

Fix triggering issues:
> My LinkedIn writing skill keeps triggering when I ask Claude to write emails. Can you fix it?

### Fix your agent context file instead

Sometimes the answer isn't a skill — it's a better `CLAUDE.md` or `AGENTS.md`:
> Claude keeps ignoring my testing conventions. I have an AGENTS.md that says to use vitest and put fixtures in \_\_fixtures\_\_ but it just does its own thing. Can you help?

The skill will recognize this as an agent context file problem and help you rewrite it using `<important if="condition">` blocks for better instruction adherence, rather than creating an unnecessary skill.

### Advanced patterns

Skill with config and memory — asks for setup on first use, remembers history:
> I want a standup skill that looks at my git commits and Linear tickets, posts to Slack, and remembers what it posted last time so it can show what changed. Different people on my team use different Slack channels — can it ask on first use?

Composable helper scripts — libraries Claude can combine for complex analysis:
> Make a data analysis skill with helper functions for querying our event warehouse, computing funnels, and flagging anomalies. Claude should be able to compose these into custom scripts on the fly for ad-hoc questions.

On-demand hooks (Claude Code only) — hooks that activate for the session:
> Make a skill I can invoke when working on our billing module that blocks any file edits outside the `packages/billing/` directory. I keep accidentally drifting into unrelated code when I'm debugging.

## Skill Structure Conventions

Skills produced by this skill follow the conventions in [`AGENTS.md`](../../AGENTS.md):

- **Frontmatter** has exactly two fields: `name` (kebab-case, matching the directory name) and `description` (trigger phrases for the skill loader)
- **SKILL.md order:** YAML frontmatter → intro → references routing table → core content
- **Progressive disclosure:** lean SKILL.md as a workflow hub (<500 lines), deep content in `references/`
- **References routing table** uses a "When…" / "Read" column pair — agent loads files on demand, not all at once
- **Reference files** are lowercase kebab-case `.md` in `references/`
- **No executable code** in SKILL.md or reference files — scripts go in `scripts/`, assets in `assets/`
- **Naming:** directories are lowercase kebab-case noun-phrases (e.g., `code-reviewer`, not `review-code`)

## Environment Support

| Feature | Claude.ai | Claude Code | Cowork |
|---------|-----------|-------------|--------|
| Skill creation wizard | Yes | Yes | Yes |
| Templates | Yes | Yes | Yes |
| Conversation extraction | Yes | Yes | Yes |
| Skill review / improve | Yes | Yes | Yes |
| Agent context file guide | — | Yes | — |
| Formal evals (subagents) | — | Yes | Yes |
| Description optimization | — | Yes | Yes |
| On-demand hooks | — | Yes | — |
