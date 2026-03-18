# Advanced Skill Patterns

These patterns go beyond basic SKILL.md + references. They leverage the full capability of the skill folder structure, Claude Code configuration options, and the filesystem as a form of context engineering.

---

## Config & Setup Pattern

Some skills need user-specific context before they can run. For example, a skill that posts standups to Slack needs to know which channel. A deploy skill needs to know the target environment.

### Pattern: Store setup in `config.json`

Put user-specific configuration in a `config.json` file in the skill directory. On first run, if the config is missing, the skill asks the user for the information and saves it.

**In your SKILL.md:**
```markdown
## Setup

Before first use, check for `config.json` in the skill directory. If it doesn't exist, ask the user for:
- Slack channel ID (e.g., #team-standup)
- Their name as it should appear in posts
- Timezone for "yesterday" calculations

Save their answers to `config.json`:

\```json
{
  "slack_channel": "#team-standup",
  "author_name": "Alex",
  "timezone": "America/Los_Angeles"
}
\```

On subsequent runs, read `config.json` and use the saved values. If a field is missing (e.g., after a skill update adds a new setting), ask for just that field.
```

### Tips

- If you want the agent to present structured, multiple-choice questions during setup, instruct Claude to use the AskUserQuestion tool.
- Keep config minimal — only store things the skill truly can't infer from context.
- Document the config fields in the SKILL.md so users can hand-edit if they prefer.

---

## Memory & Storing Data

Skills can maintain state between runs by storing data in files. This is powerful for skills that benefit from history — knowing what happened last time, tracking patterns over time, or avoiding duplicate work.

### Storage options

**Append-only log files** — simplest. Good for standups, recaps, or any skill that benefits from knowing what it said before.
```
standups.log
─────────────
2026-03-10: Shipped auth refactor, started billing migration
2026-03-11: Billing migration 60%, blocked on API rate limits
2026-03-12: Unblocked, migration complete. Starting test coverage push.
```

**JSON files** — structured data. Good for tracking state, scores, or configuration that evolves.
```json
{
  "last_run": "2026-03-12T09:00:00Z",
  "total_runs": 47,
  "last_report_path": "reports/2026-03-12.md"
}
```

**SQLite databases** — for complex data relationships or when you need queries. Good for data analysis skills that accumulate findings over time.

### Where to store data

Data stored in the skill directory itself may be deleted when the skill is upgraded. For persistent data, use the `${CLAUDE_PLUGIN_DATA}` environment variable — this is a stable folder per plugin that survives upgrades.

**In your SKILL.md:**
```markdown
## Data Storage

Store run history in `${CLAUDE_PLUGIN_DATA}/history.json`. If the directory doesn't exist, create it. If the file doesn't exist, initialize it as an empty array.

After each run, append an entry:
\```json
{
  "timestamp": "2026-03-12T09:00:00Z",
  "summary": "one-line summary of what was done",
  "output_path": "path/to/output/if/applicable"
}
\```

Read history at the start of each run so you know what changed since last time.
```

### Tips

- Keep stored data lean. A standup log doesn't need full transcripts — one line per day is enough.
- For log files, periodically rotate or truncate to avoid unbounded growth.
- Make the skill work gracefully when data is missing (first run or after a reset).

---

## Composable Scripts & Code Generation

One of the most powerful things you can give Claude is code. Scripts and libraries let Claude spend its turns on composition and decision-making rather than reconstructing boilerplate.

### Pattern: Helper libraries Claude can compose

Instead of just single-purpose scripts, provide a library of composable helper functions. Claude can then import and combine them to build more complex analyses on the fly.

**Example: data analysis skill**
```python
# scripts/helpers.py

def fetch_events(event_type: str, start: str, end: str) -> pd.DataFrame:
    """Fetch events from the analytics warehouse."""
    conn = get_warehouse_connection()
    return pd.read_sql(f"""
        SELECT * FROM events
        WHERE event_type = '{event_type}'
        AND timestamp BETWEEN '{start}' AND '{end}'
    """, conn)

def compute_funnel(events: pd.DataFrame, steps: list[str]) -> dict:
    """Compute conversion funnel from a sequence of event types."""
    results = {}
    for i, step in enumerate(steps):
        count = events[events.event_type == step].user_id.nunique()
        results[step] = {
            "users": count,
            "conversion": count / results[steps[0]]["users"] if i > 0 else 1.0
        }
    return results

def flag_anomalies(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """Flag values that are more than threshold * stddev from the mean."""
    mean, std = series.mean(), series.std()
    return series.apply(lambda x: abs(x - mean) > threshold * std)
```

**In your SKILL.md:**
```markdown
## Available Helper Functions

The `scripts/helpers.py` module provides reusable functions for common data tasks.
Import them in any generated script:

- `fetch_events(event_type, start, end)` — query the analytics warehouse
- `compute_funnel(events, steps)` — calculate conversion funnel
- `flag_anomalies(series, threshold)` — detect statistical outliers

For complex analysis, generate a new script that composes these helpers.
For example, to answer "What happened on Tuesday?", generate a script that
fetches the relevant events, computes the funnel, and flags anomalies.
```

### Pattern: Script architecture (deterministic vs LLM tasks)

Separate deterministic tasks from judgment tasks upfront:

- **Scripts handle:** math, file parsing, data validation, CSV generation, format conversion, API calls — anything with one correct answer that can be computed.
- **LLM handles:** categorization where context matters, narrative generation, interpreting ambiguous inputs, generating human-readable summaries.

This separation makes skills reliable across hundreds of runs instead of subtly varying each time.

### Tips

- Design scripts with CLI interfaces (`--input`, `--output`, `--help` flags) so they're reusable and testable independently of the skill.
- When multiple test runs independently write similar helper scripts, that's a strong signal the skill should bundle that script.
- Scripts can execute without being loaded into context, which saves token budget.

---

## On-Demand Hooks

> **Environment:** On-demand hooks are a Claude Code feature. They are not available on Claude.ai.

Skills can include hooks that are only activated when the skill is called, and last for the duration of the session. Use this for opinionated hooks that you don't want running all the time but are extremely useful sometimes.

### Examples

**`/prod-mode` — production guardrails:**
Blocks destructive Bash commands (`rm -rf`, `DROP TABLE`, force-push, `kubectl delete`) via a PreToolUse matcher. You only want this active when you know you're touching production — having it always on would be too noisy for normal development.

**`/focus` — edit restrictions:**
Blocks any Edit/Write outside a specific directory. Useful when debugging a module: you want to add instrumentation but keep accidentally "fixing" unrelated code in other parts of the codebase.

### How to implement

In your skill's configuration, register hooks that activate when the skill is invoked:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "script": "scripts/check_dangerous_commands.sh"
      }
    ]
  }
}
```

**In your SKILL.md:**
```markdown
## Hooks

This skill registers a PreToolUse hook that checks Bash commands against
a blocklist of dangerous patterns. If a match is found, the hook rejects
the command and explains why.

The hook is only active while this skill is in use.
```

### Tips

- Keep hook scripts fast — they run on every matching tool call.
- Make the rejection message helpful: explain *why* the command was blocked and suggest an alternative.
- Test hooks independently before bundling them in the skill.

---

## Skill Composition

Skills can reference other skills by name. Claude will invoke them if they're installed. This enables building higher-level workflows from smaller, focused skills.

**Example:** A `gradual-rollout` skill might reference a `smoke-tests` skill and a `post-to-slack` skill:

```markdown
## Rollout Steps

1. Build and tag the release
2. Run smoke tests (use the `smoke-tests` skill if installed)
3. Shift 5% of traffic to the new version
4. Notify the team (use the `post-to-slack` skill if installed)
5. Monitor error rate for 10 minutes
6. If error rate is within threshold, promote to 100%
```

Dependency management between skills is not built into the marketplace yet, so reference other skills as optional enhancements rather than hard requirements. The skill should still work (perhaps with reduced functionality) if a referenced skill is not installed.
