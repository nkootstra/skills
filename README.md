# Skills

AI agent skills for Claude Code that extend your assistant's capabilities.

## Installation

```bash
npx skills add nkootstra/skills
```

Browse and install available skills into your project.

## Available Skills

| Skill | Description |
|-------|-------------|
| **adversarial-review** | Set up multi-agent adversarial verification pipelines (bug-finder → adversary → referee) for high-fidelity code review and bug detection. Adapts to both Claude Code CLI and Claude.ai. |
| **agents-md** | Write, audit, and improve AGENTS.md files. Produces minimal, high-signal context that earns its cost on every session. |
| **code-complexity-audit** | Scan and analyze a repository for design quality using principles from A Philosophy of Software Design. Evaluates module depth, abstraction quality, information hiding, and complexity patterns. |
| **compact-markdown** | Compact/minify markdown to fewer tokens w/ zero information loss. Five ordered passes: collapse, terse, trim, symbols, formatting. |
| **context-guardian** | Helps developers keep agent context lean and focused for maximum performance. Covers context audits, research/implementation splits, session drift recovery, and prompt crafting. |
| **create-skill** | Create, improve, and manage Claude skills through a guided wizard, starter templates, or by converting conversation history into reusable skills. Also covers running evals and benchmarking skill performance. |
| **latency-engineering** | Diagnose and reduce latency in software systems. Use when dealing with slow APIs, tail latency, p99 spikes, caching, replication, partitioning, concurrency, async I/O, or any question about making systems faster. |
| **pie-design-system** | PIE (Just Eat Takeaway) design system expert. Guides component selection, correct import paths for Web Components and React wrappers, design token application, and framework setup (React, Next.js, Vue, Nuxt). |
| **python-best-practices** | Comprehensive Python expertise covering language fundamentals, idiomatic patterns, software design principles, and production best practices. |
| **zig-best-practices** | Comprehensive guide for writing, reviewing, and improving Zig code following idiomatic patterns and best practices. Covers allocators, comptime, error handling, build system, C interop, and performance. |

## License

MIT
