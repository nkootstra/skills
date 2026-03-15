---
name: create-skill
description: Create, improve, and manage Claude skills through a guided wizard, starter templates, or by converting conversation history into reusable skills. Use this skill whenever the user mentions creating a skill, building a skill, "turn this into a skill", "make a skill from this", skill templates, improving an existing skill, running skill evals, benchmarking skill performance, optimizing skill descriptions, or anything related to authoring or editing SKILL.md files. Also trigger when the user says things like "I keep repeating myself", "Claude should remember this", "automate this workflow", or "save this as a process". Even if the user doesn't use the word "skill", trigger when they want to codify a repeatable process for Claude. This includes non-developers, designers, writers, and anyone who wants Claude to work the way they do without re-explaining every time.
---

# Skill Creator Plus

An enhanced skill creation system that extends the [official Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator). It adds three layers on top: a guided wizard for non-developers, a starter templates library, and the ability to extract skills directly from conversation history.

Think of it this way: Claude already knows how to cook. A skill is a recipe — it tells Claude exactly what dish to make, what ingredients to use, and how you like it served. This skill helps you write those recipes.

**The rule of thumb:** if you repeat any process with Claude more than twice, that process should probably be a skill.

At a high level, creating a skill goes like this:

- Decide what the skill should do and roughly how
- Write a draft of the SKILL.md
- Create a few test prompts and run them
- Evaluate the results with the user (qualitatively and quantitatively)
- Rewrite the skill based on feedback
- Repeat until satisfied
- Optimize the description for reliable triggering
- Package and share

Your job is to figure out where the user is in this process and help them progress. Maybe they say "I want to make a skill for X" — help them narrow it down, draft it, test it. Maybe they already have a draft — jump straight to eval/iterate. Maybe they say "I don't need formal evaluations, just vibe with me" — that's fine too, be flexible.

---

## Read the Situation First

Before doing anything, assess what the user actually needs. This is the most important step — it determines everything else.

**Read these signals:**

- **User already has a draft?** → Skip the wizard. Go straight to review/diagnose mode (Path 4).
- **User says "turn this into a skill"?** → Use conversation extraction (Path 3).
- **Request is trivially simple?** (e.g., "just add a signature to my emails") → Don't force 8 wizard steps. Generate a minimal skill immediately. Match the skill's complexity to the task's complexity — a 1-line behavior gets a 10-line skill, not a 150-line monstrosity.
- **Request is complex with many steps?** → Full wizard flow. Take your time on edge cases and scripts.
- **Request is vague?** (e.g., "help me set up stuff faster") → Use the wizard to draw out specifics. Don't generate anything until you understand the actual workflow.
- **User is frustrated with a broken skill?** → Don't re-ask questions they already answered. Acknowledge the problem, diagnose directly, and fix it.
- **Requirements contradict each other?** → Surface the tension before generating. A skill built on contradictions will produce inconsistent output.
- **Request overlaps with something Claude already does well?** → Probe for what the skill adds beyond default behavior. If the user has specific format/style preferences, create the skill. If not, gently explain that Claude already handles this.

**Scale your response to the task:**
- Trivial tasks → minimal skill, fast turnaround
- Clear tasks → wizard with appropriate depth, skip unnecessary steps
- Complex tasks → full wizard, edge cases, scripts architecture, test cases
- Vague tasks → discovery questions first, skill later

## Communicating with the User

Skills attract people across a wide range of technical backgrounds. Non-developers, designers, writers, and makers are building skills alongside experienced engineers. Pay attention to context cues and adapt your language accordingly.

Default to plain language. Some guidelines:

- "evaluation" and "benchmark" are borderline but OK for most people
- For "JSON" and "assertion", wait for signals that the user knows these terms before using them without explanation
- It's always OK to briefly explain a term if you're unsure

When explaining skills to someone new: "A skill is a set of instructions you write once, and Claude follows them every time. No more re-explaining your preferences — you teach Claude how you work, and it remembers."

When describing output to others, lead with outcomes: "This skill lets you generate consistent weekly reports in 30 seconds" beats "This skill contains YAML frontmatter and Markdown instructions for report generation."

### Handling Pushback

Sometimes users push back on suggestions, want to skip steps, or get frustrated. That's fine — don't force the process.

- If a user says "just make it, stop asking questions" → draft something reasonable and let them react. "Got it — I'll draft it and you can tell me if it lands. Easy to adjust from there."
- If a user rejects a template → start from scratch without friction. "No problem — let's build it from the ground up."
- If a user is frustrated with a broken skill → acknowledge the issue directly, diagnose fast, and don't over-apologize. "I can see both problems clearly. Let me fix them."

The wizard is a guide, not a gate. Users should be able to skip steps that don't add value for their specific case.

---

## Four Ways to Create or Improve a Skill

When a user wants to create or improve a skill, figure out which path fits best:

### Path 1: Guided Wizard (default for new skills)

Use this when the user says something like "I want to create a skill" or "help me build a skill" and doesn't already have a draft. Walk them through a structured interview — no jargon, no assumptions about technical background.

**The wizard flow:**

**Step 1 — What does it do?**
Ask: "What do you want Claude to do for you automatically? Describe it like you're explaining to a colleague."

Listen for the core task. Restate it back in one sentence to confirm. Don't move on until you both agree on what the skill does.

**Watch for contradictions** when restating. If the requirements pull in opposite directions (e.g., "thorough but concise", "detailed but short", "comprehensive but minimal"), surface the tension diplomatically before proceeding. Common contradictions: thoroughness vs brevity, flexibility vs consistency, simplicity vs feature-richness. Offer resolution paths: two modes in one skill, layered output (TL;DR + full version), or two separate skills. Let the user decide — but don't build a skill on contradictory foundations, because it will produce inconsistent output across runs.

**Watch for overlap** with Claude's built-in abilities. If the task is something Claude already does well by default (summarizing, translating, basic code review, email drafting), probe for what the skill would add: "Claude already handles [task] pretty well out of the box. What's missing from how it does it now — is there a specific format, style, or process you want locked in?" If the user has specific requirements, the skill is justified. If not, gently explain the skill would add overhead without improving output.

**Step 2 — When should it activate?**
Ask: "What would you say to Claude that should make this kick in? Give me 2-3 example sentences you'd type."

These become the trigger phrases for the description. Also ask: "Is there anything similar that should NOT trigger this?" — this helps write a precise description that avoids false positives.

**Step 3 — What does good output look like?**
Ask: "Can you show me an example of what you'd want Claude to produce? Or describe what the ideal result looks like?"

If they have an example, use it as a reference. If not, ask about format (document, code, structured text?), length, tone, and any must-haves.

**Step 4 — Any rules or preferences?**
Ask: "Are there things Claude should always do or never do when running this skill?"

These become constraints in the instructions. Common ones: always use a specific tone, never include certain content, always structure output a certain way.

**Step 5 — Should we test it formally?**
Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art direction) are often better evaluated by human judgment alone. Suggest the appropriate default based on the skill type, but let the user decide.

**Step 6 — Edge cases and dependencies**
Proactively ask about edge cases, input/output formats, example files, success criteria, and dependencies. Check available MCPs — if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

Wait to write test prompts until you've ironed this part out.

**Step 7 — Pick a starting point**
Based on what you've learned, check if one of the built-in templates (see `templates/` directory) is a close fit. If so, offer it: "This sounds like a [content writer / document generator]. I have a starter template for that — want me to use it as a base, or start from scratch?"

If no template fits, start from a blank SKILL.md.

**Step 8 — Generate the draft**
Write the SKILL.md based on everything gathered. Show it to the user and explain each section briefly in plain language. Ask: "How does this look? Anything you'd change?"

Then proceed to the testing phase (see "Testing and Iteration" below).

---

### Path 2: Templates (fast start for common patterns)

Use this when the user's need maps clearly to a common pattern, or when they ask "do you have any templates?" or "what kinds of skills can I make?"

Templates live in the `templates/` directory. Read the relevant template file and use it as scaffolding — fill in the user's specific details while keeping the proven structure.

**Available templates:**

| Template | File | Best for |
|----------|------|----------|
| Content Writer | `templates/content-writer.md` | Blog posts, social media, newsletters, any writing with a consistent voice |
| Document Generator | `templates/document-generator.md` | Reports, decks, proposals, memos — structured docs with consistent formatting |

When presenting templates, describe them by what they help the user accomplish, not by their internal structure. For example: "I have a Content Writer template that's great for keeping a consistent voice across blog posts and social media. Want me to customize it for you?"

After selecting a template, walk through the customization: fill in their specific voice, format preferences, examples, and constraints. The template provides the skeleton; the user provides the soul.

**The three common skill patterns** (knowing which type helps write better instructions):

1. **Document and asset creation.** Creating things that look and feel consistent every time — presentations, reports, code, designs. The skill embeds style guides, templates, and quality checklists.
2. **Workflow automation.** Multi-step processes that repeat often. The skill walks Claude through each step so nothing gets skipped.
3. **MCP enhancement.** Claude is already connected to external tools (Notion, Linear, Figma, etc.) through MCP. The skill adds a guidance layer — it doesn't give Claude new tools, it teaches Claude *how to use existing tools for a specific workflow*. When building MCP-enhanced skills:
   - Reference the specific MCP tool capabilities in the instructions (e.g., "Use the Notion MCP to query the Backlog database with filter: Status = 'Ready'")
   - Include tool-specific patterns (Notion relation properties behave differently from text fields; Figma components have different access patterns than frames)
   - Handle MCP unavailability gracefully: tell the user the connection is needed, suggest checking settings, and don't fake the workflow without the tools
   - Be aware of rate limits when making many API calls (e.g., updating 50 tasks in a sprint) — batch updates and add pauses

---

### Path 3: Conversation-to-Skill ("Turn this into a skill")

Use this when the user says "turn this into a skill", "save this as a skill", "make a skill from this conversation", or similar. The idea is to extract a repeatable pattern from what just happened in the conversation.

**How to extract a skill from conversation history:**

1. **Scan the conversation** for patterns: What did the user ask Claude to do? What corrections did they make? What format did they settle on? What tools were used? What was the final output?

2. **Identify the repeatable core.** Not everything in a conversation is skill-worthy. Look for: the stable workflow (steps that would be the same next time), the user's preferences (tone, format, structure), the tools and techniques used, and any corrections that reveal implicit rules.

3. **Draft the skill** based on what you extracted. Structure it as:
   - Goal: what the skill accomplishes
   - Trigger: when it should activate (based on how the user initiated the conversation)
   - Steps: the workflow, incorporating corrections the user made
   - Output format: based on what the user accepted as good
   - Constraints: based on corrections and stated preferences

4. **Show the user what you extracted** before generating the SKILL.md. Say something like: "Here's what I picked up from our conversation: [summary]. Does this capture the process you want to repeat?"

5. **Generate the SKILL.md** after confirmation. Then offer to test it.

This path is powerful because it captures implicit knowledge — the stuff users don't think to write down but always correct for.

---

### Path 4: Review and Improve an Existing Skill

Use this when the user already has a SKILL.md and wants it reviewed, fixed, or improved. They might say "review my skill", "fix my skill", "it's inconsistent", "it triggers for the wrong things", or paste an existing SKILL.md with complaints.

**Do NOT re-run the wizard.** The user already has something — they want diagnosis, not a restart.

**How to review an existing skill:**

1. **Read the SKILL.md carefully.** Before running any tests, look for common problems:
   - **Thin description** — fewer than 3 trigger phrases almost guarantees undertriggering
   - **Vague instructions** — phrases like "be thorough but not nitpicky" or "use good judgment" produce inconsistent output because Claude interprets them differently each run
   - **Missing output format example** — abstract descriptions of format ("a numbered list with severity") vary across runs; concrete examples lock it in
   - **No edge case handling** — the skill works for the happy path but fails on unusual inputs
   - **Overly broad triggering** — description matches too many contexts (e.g., "writes professional content" triggers on emails when it should only trigger on LinkedIn posts)

2. **Diagnose and rank problems.** Tell the user what you found, ordered from most impactful to least. Be specific: "Your description says 'Reviews code' — that's 2 words. A developer saying 'check my Python script for performance issues' might not trigger this because the description doesn't mention Python, performance, or scripts."

3. **Propose fixes with reasoning.** Don't just rewrite — explain why each change matters. The user learns to write better skills, and they can push back if they disagree with the reasoning.

4. **Preserve the user's intent and structure.** Improve the skill, don't rebuild it from scratch. The user has context about their workflow that you don't — respect it.

5. **Offer to test after.** "Want me to run your original prompt through this improved version so you can compare?"

---

## Writing the SKILL.md

Regardless of which path you took to get here, every skill follows the same structure.

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### Progressive Disclosure

Skills use a three-level loading system. Understanding this helps you write efficiently:

1. **Metadata** (name + description) — Always in Claude's context (~100 words). This is what triggers the skill.
2. **SKILL.md body** — Loaded into context whenever the skill triggers (<500 lines ideal).
3. **Bundled resources** — Loaded as needed (unlimited size; scripts can execute without being loaded into context).

This means the description carries all the triggering weight, the SKILL.md body carries the instructions, and heavy reference material goes in separate files.

### Frontmatter

```yaml
---
name: kebab-case-name
description: [What it does] + [When to trigger — be pushy] + [Key capabilities].
---
```

The description is the single most important line. Claude uses it to decide whether to load the skill. Claude currently has a tendency to "undertrigger" — to not use skills when they'd be useful. To combat this, make descriptions a little "pushy." Include specific phrases users would say, and err on the side of triggering too much rather than too little.

**Good description formula:** `[What it does] + [When to use it] + [Key capabilities]`

**Example of a pushy description:**
Instead of: "How to build a simple fast dashboard to display internal data."
Write: "How to build a simple fast dashboard to display internal data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"

All "when to use" info goes in the description, not in the body — the body isn't loaded until after the triggering decision has already been made.

**Include negative triggers when relevant.** If the skill is for a specific context that could be confused with related contexts, explicitly exclude them in the description. For example, a LinkedIn writing skill should say "Do NOT trigger for emails, Slack messages, tweets, or any non-LinkedIn writing." This prevents false positives that frustrate users. Also consider adding a "What This Skill Does NOT Do" section in the instructions body for clarity.

### Instructions Body

Write in plain Markdown. Use the imperative form. Explain *why* things matter, not just *what* to do — Claude is smart and responds better to reasoning than to rigid commands.

**Structure pattern:**
```markdown
# Skill Name

## What This Skill Does
One paragraph explaining the purpose.

## Instructions

### Step 1: [Action]
What to do and why it matters.

### Step 2: [Action]
What to do and why it matters.

## Output Format
What the final result should look like. Include an example if possible.

## Common Pitfalls
Things that tend to go wrong and how to handle them.
```

**Writing patterns:**

Defining output formats:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

Including examples (these are very useful for Claude):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

**Key writing principles:**

- **Explain the why.** Instead of "ALWAYS use bullet points", write "Use bullet points for lists of 3+ items because the reader will scan these sections quickly and bullets improve readability." Try to explain why things are important rather than using heavy-handed MUSTs. Use theory of mind and aim for general, not super-narrow instructions. Today's LLMs are smart — they have good theory of mind and when given a good harness can go beyond rote instructions.

- **Put critical info first.** Claude pays most attention to instructions near the top. If something is non-negotiable, don't bury it.

- **Include examples of good output.** One concrete example is worth ten paragraphs of description. If you can show what "good" looks like, do it.

- **Keep it under 500 lines.** If you're approaching this limit, add an additional layer of hierarchy with clear pointers about where to find details. Split heavy content into reference files in a `references/` subdirectory and point to them from SKILL.md with guidance on when to read them. For large reference files (>300 lines), include a table of contents.

- **Be specific about output format.** Instead of "write a professional report", spell out the exact sections, tone, and length you expect.

- **Write a draft, then improve it.** Start by writing a draft and then look at it with fresh eyes. Try to make the skill general and not super-narrow to specific examples.

**Domain organization:** When a skill supports multiple domains or frameworks, organize by variant so Claude reads only the relevant reference:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### Bundled Resources

Use **scripts** when a task is deterministic and repeatable (data validation, file conversion, formatting, calculations). Scripts can execute without being loaded into context, which saves space.

**Proactive script architecture:** Don't wait for test runs to reveal the need for scripts. When designing a skill with multi-step data processing, separate the work upfront:
- **Scripts handle deterministic tasks:** math, file parsing, data validation, CSV generation, format conversion — anything with one correct answer that can be computed.
- **LLM handles judgment tasks:** categorization where context matters, narrative generation, interpreting ambiguous inputs, generating human-readable summaries.

This separation is the difference between a skill that's reliable across hundreds of runs and one that subtly varies each time. When the user says "I don't want Claude reinventing the wheel every time," they're asking for scripts.

Design scripts with CLI interfaces (`--input`, `--output`, `--help` flags) so they're reusable and testable independently of the skill.

Use **references** for large bodies of knowledge that the skill needs sometimes but not always. Point to them from SKILL.md with clear guidance on when to read them.

Use **assets** for files that get embedded in output (templates, images, fonts, icons).

### Principle of Lack of Surprise

Skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Roleplay-style skills ("roleplay as XYZ") are fine.

---

## Testing and Iteration

After drafting a skill, test it. This is where real quality comes from — skills get better through iteration, not through perfect first drafts.

### Test Cases

Come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?"

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

### Quick Test (Claude.ai)

Claude.ai doesn't have subagents, so some mechanics change. Here's the adapted workflow:

**Running test cases:** No parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — the human review step compensates. Skip baseline runs.

**Reviewing results:** If you can't open a browser (e.g., Claude.ai's VM has no display), skip the browser reviewer. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file (.docx, .xlsx, etc.), save it and tell the user where to download it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking:** Skip quantitative benchmarking — it relies on baseline comparisons that aren't meaningful without subagents. Focus on qualitative feedback.

**The iteration loop:** Same as always — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem.

**Common fixes during iteration:**
- Skill doesn't trigger → improve the description (add more trigger phrases, be pushier)
- Output format is wrong → add more specific format instructions or an example
- Missing steps → add them, with reasoning for why they matter
- Tone is off → add voice/style examples with both good and bad examples

### Full Eval (Claude Code / environments with subagents)

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

**Step 1: Spawn all runs (with-skill AND baseline) in the same turn**

For each test case, spawn two subagents in the same turn — one with the skill, one without. Don't spawn the with-skill runs first and then come back for baselines. Launch everything at once so it all finishes around the same time.

With-skill run:
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

Baseline run (same prompt, but the baseline depends on context):
- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case. Give each eval a descriptive name based on what it's testing — not just "eval-0". If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

**Step 2: While runs are in progress, draft assertions**

Don't just wait — use this time to draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable and have descriptive names that read clearly in the benchmark viewer.

Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with assertions once drafted. Explain to the user what they'll see in the viewer.

**Step 3: As runs complete, capture timing data**

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory — this is the only opportunity to capture it. It comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

**Step 4: Grade, aggregate, and launch the viewer**

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it.

2. **Aggregate into benchmark:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <n>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects. Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` for what to look for: non-discriminating assertions, high-variance evals, time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, pass `--previous-workspace <workspace>/iteration-<N-1>`.

   Always use `generate_review.py` to create the viewer — don't write custom HTML. GENERATE THE EVAL VIEWER *BEFORE* evaluating outputs yourself. Get results in front of the human ASAP.

**Step 5: Read the feedback**

When the user tells you they're done reviewing, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus improvements on test cases with specific complaints.

Kill the viewer server when done: `kill $VIEWER_PID 2>/dev/null`

### What the User Sees in the Viewer

The "Outputs" tab shows one test case at a time: the prompt, the files the skill produced (rendered inline where possible), formal grades if grading was run, a feedback textbox, and previous feedback from earlier iterations. Navigation is via prev/next buttons or arrow keys.

The "Benchmark" tab shows stats: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

When done, the user clicks "Submit All Reviews" which saves all feedback to `feedback.json`.

### Cowork-Specific Instructions

If you're in Cowork:

- You have subagents, so the main workflow works (spawn in parallel, run baselines, grade, etc.). If timeouts are a problem, run test prompts in series.
- No browser/display — use `--static <output_path>` for the eval viewer to write a standalone HTML file. The user can open it in their browser.
- The "Submit All Reviews" button downloads `feedback.json` as a file. Read it from the Downloads folder (you may need to request access).
- Packaging works — `package_skill.py` needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) works since it uses `claude -p` via subprocess.
- Save description optimization until the skill is fully finished and the user agrees it's in good shape.

---

## Improving the Skill

This is the heart of the loop. You've run test cases, the user has reviewed results, and now you need to make the skill better.

### How to Think About Improvements

1. **Generalize from the feedback.** Skills will be used across many different prompts. You and the user are iterating on only a few examples because it's faster. But if the skill only works for those examples, it's useless. Rather than fiddly overfitting changes or oppressively constrictive MUSTs, try branching out with different metaphors or patterns if something is stubborn. It's relatively cheap to try.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read transcripts, not just final outputs — if the skill is making Claude waste time on unproductive steps, get rid of what's causing that.

3. **Explain the why.** Try hard to explain the reasoning behind everything the skill asks. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — reframe as reasoning. "Always validate the date format" → "Validate the date format because downstream systems reject non-ISO dates and the user won't see the error until much later." That's more humane, powerful, and effective.

4. **Look for repeated work across test cases.** Read transcripts and notice if all test runs independently wrote similar helper scripts or took the same multi-step approach. If all 3 test cases resulted in writing a `create_docx.py` or `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task matters — take your time and really think it through. Write a draft revision and then look at it anew and make improvements. Get into the head of the user and understand what they want and need.

### The Iteration Loop

After improving the skill:

1. Apply improvements
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. For a new skill, the baseline is always `without_skill`. For an existing skill, use judgment on the baseline: the original version or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for user review
5. Read feedback, improve, repeat

Keep going until the user is happy, feedback is all empty, or you're not making meaningful progress.

### Advanced: Blind Comparison

For situations where you want rigorous comparison between two skill versions ("is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for details. The idea: give two outputs to an independent agent without revealing which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

After the skill is working well, offer to optimize the description for better triggering accuracy.

### How Skill Triggering Works

Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. Important: Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means eval queries should be substantive enough that Claude would actually benefit from consulting the skill. Simple queries like "read file X" are poor test cases.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic and specific — include file paths, personal context, column names, company names, URLs, backstory. Use a mix of lengths. Some might be lowercase with abbreviations, typos, or casual speech. Focus on edge cases rather than clear-cut examples.

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For **should-trigger** queries (8-10): cover different phrasings of the same intent — formal, casual, implicit. Include cases where the user doesn't name the skill or file type but clearly needs it. Include uncommon use cases and cases where this skill competes with another.

For **should-not-trigger** queries (8-10): the most valuable are near-misses — queries that share keywords or concepts but need something different. Think adjacent domains, ambiguous phrasing where keyword matching would trigger but shouldn't. Avoid obviously irrelevant queries — "write a fibonacci function" as a negative for a PDF skill is too easy.

### Step 2: Review with user

Present the eval set for review using the HTML template:
1. Read the template from `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` → JSON array, `__SKILL_NAME_PLACEHOLDER__` → name, `__SKILL_DESCRIPTION_PLACEHOLDER__` → description
3. Write to a temp file and open it
4. User edits, then clicks "Export Eval Set"
5. Check Downloads folder for the JSON

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background."

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt so the triggering test matches what the user actually experiences. While it runs, periodically tail output to give updates.

The loop automatically splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times for reliability), then calls Claude to propose improvements based on failures. It iterates up to 5 times and returns JSON with `best_description` — selected by test score to avoid overfitting.

Note: Description optimization requires the `claude` CLI tool (`claude -p`), which is only available in Claude Code and Cowork. Skip it on Claude.ai.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.

---

## Updating an Existing Skill

The user might ask to update an existing skill, not create a new one. In this case:

- **Don't re-run the full wizard.** The user already has context — diagnose what's wrong and fix it. See Path 4 for the review approach.
- **Preserve the original name.** Note the skill's directory name and `name` frontmatter field — use them unchanged. If the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory — direct writes may fail due to permissions.
- **Don't re-ask questions the user already answered.** If they said "the tone is too formal, make it casual" — that's the instruction. Don't respond with "What should this skill enable Claude to do?" A frustrated user who already explained the problem doesn't want to re-explain it through 4 generic questions.

---

## Packaging and Sharing

When the skill is ready:

### Package it

Check whether you have access to the `present_files` tool. If so, package and present:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Direct the user to the resulting `.skill` file path so they can install it.

### Installation

- **Personal use:** Install in Claude Settings → Capabilities → Skills. Upload the skill folder.
- **Team use:** Admins can deploy skills across an entire workspace so all team members get the same skill behavior automatically. When building skills for teams, prioritize consistency: use rigid output frameworks (not "use your judgment"), embed team-specific references directly (don't leave "[add your principles here]" placeholders), and make the structure explicit enough that output from any team member is comparable. If 8 people should all produce critiques in the same format, the format must be locked down in the skill, not left to individual interpretation.
- **Claude Code:** Place the folder in your skills directory.
- **Public sharing:** Host the skill folder on GitHub with a clear README explaining what it does, how to install it, and what it looks like in action.

### Managing Skills with Obsidian

Skills are just Markdown files, and Obsidian is excellent for managing them. If you use Obsidian, consider storing skills in a `Skills/` folder in your vault. You can browse skills alongside notes, edit them instantly with clean formatting, and link skills to related notes like voice guides, content pillars, or reference examples. Everything stays connected in one system. Claude Code also works directly with Obsidian vaults, so your skill library and knowledge base can live in the same place.

---

## Reference Files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent:

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json, timing.json, comparison.json, analysis.json, metrics.json

The templates/ directory has starter templates:
- `templates/content-writer.md` — Template for voice/tone consistent writing skills
- `templates/document-generator.md` — Template for structured document generation skills

If you're in an environment with access to agents and scripts (Claude Code, Cowork), use them. If not (Claude.ai), use the simplified testing approach.

---

## Quick Reference: The Core Loop

1. **Understand** — What does the user want? (wizard interview, template selection, or conversation extraction)
2. **Draft** — Write the SKILL.md with proper frontmatter, clear instructions, and examples
3. **Test** — Run 2-3 realistic prompts through the skill
4. **Review** — Show results to the user, get feedback (use `eval-viewer/generate_review.py` if available)
5. **Improve** — Update the skill based on feedback, generalizing rather than overfitting
6. **Repeat** — Until the user is happy
7. **Optimize** — Fine-tune the description for reliable triggering
8. **Package** — Bundle, present, and share

Please add steps to your TodoList if you have one. If you're in Cowork, specifically add "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" to make sure it happens.

Good luck!
