# Code Scaffolding Template

Use this template when building a skill that generates boilerplate for new components, services, features, or projects. These skills are especially useful when the scaffolding involves decisions beyond what a pure code template can express — naming conventions, integration points, configuration, or documentation that varies by context.

## How to Customize

Replace everything in `[brackets]` with the user's specifics. Delete sections that don't apply.

---

## Template SKILL.md

```markdown
---
name: new-[thing]
description: Scaffolds a new [thing] with [your org's] standard structure, configuration, and integrations. Use when user asks to "create a new [thing]", "scaffold a [thing]", "set up a new [thing]", "bootstrap a [thing]", or mentions starting a new [thing] from scratch. Also trigger for "add a new [component/service/feature]" or "initialize [thing]".
---

# New [Thing] Scaffolder

## What This Creates

A new [thing] with:
- [e.g., "Standard directory structure following our monorepo conventions"]
- [e.g., "Auth middleware pre-configured"]
- [e.g., "Logging and error handling wired in"]
- [e.g., "CI/CD pipeline configuration"]
- [e.g., "README with setup instructions"]

## Required Information

Before scaffolding, gather from the user:
1. **Name:** [naming convention, e.g., "kebab-case, must be unique across the monorepo"]
2. **Type/variant:** [if applicable, e.g., "API service, background worker, or scheduled job"]
3. [Any other decisions, e.g., "Database needed? Which auth provider?"]

## Scaffolding Steps

### Step 1: Create the directory structure

Use the template in `assets/[thing]-template/` as the base. Copy it to `[target path]/{name}/`.

```
{name}/
├── src/
│   ├── index.ts
│   ├── [main entry point]
│   └── [standard subdirectories]
├── tests/
│   └── [test setup files]
├── [config files]
└── README.md
```

### Step 2: Customize configuration

Replace template placeholders with the user's specifics:
- `{{NAME}}` → the chosen name
- `{{DESCRIPTION}}` → one-line description from the user
- [Other placeholders specific to your template]

### Step 3: Wire integrations

- [e.g., "Register the new service in the monorepo's workspace config"]
- [e.g., "Add to the CI pipeline matrix"]
- [e.g., "Create the initial database migration if database was requested"]

### Step 4: Validate

Run these checks to confirm the scaffold is correct:
- [e.g., "`turbo build --filter={name}` succeeds"]
- [e.g., "`turbo test --filter={name}` passes with the default test"]
- [e.g., "Lint passes with no errors"]

## Post-Scaffold Guidance

After scaffolding, tell the user:
- [e.g., "Your new service is at `apps/{name}/`. Run `turbo dev --filter={name}` to start it."]
- [e.g., "Next steps: add your routes in `src/routes/`, update the README, and push for CI."]
- [e.g., "The default test in `tests/` is a smoke test — replace it with real tests as you build."]

## Gotchas

- [e.g., "The monorepo workspace config must be updated manually — `turbo` won't pick up the new package until you run `pnpm install`"]
- [e.g., "Auth middleware expects a `JWT_SECRET` env var — add it to `.env.local` before running"]
- [e.g., "If you're adding a database, run `turbo db:generate` after creating the schema"]
```

---

## Customization Checklist

When filling in this template, make sure you've captured:

- [ ] Complete directory structure with explanation of each part
- [ ] All template placeholders and what replaces them
- [ ] Integration steps (registering in monorepo, CI, etc.)
- [ ] Validation commands to confirm the scaffold works
- [ ] Post-scaffold guidance (what to do next)
- [ ] Gotchas (common issues after scaffolding)
- [ ] Template files in `assets/` for the base structure
- [ ] Scripts in `scripts/` for any automation (file creation, config patching)
