---
name: create-skill
description: Create, improve, and manage Claude skills through a guided wizard, starter templates, or by converting conversation history into reusable skills. Use this skill whenever the user mentions creating a skill, building a skill, "turn this into a skill", "make a skill from this", skill templates, improving an existing skill, running skill evals, benchmarking skill performance, optimizing skill descriptions, or anything related to authoring or editing SKILL.md files. Also trigger when the user says things like "I keep repeating myself", "Claude should remember this", "automate this workflow", or "save this as a process". Even if the user doesn't use the word "skill", trigger when they want to codify a repeatable process for Claude. This includes non-developers, designers, writers, and anyone who wants Claude to work the way they do without re-explaining every time. Also trigger when the user wants to improve or write an agent context file: CLAUDE.md, AGENTS.md, .cursorrules, or any file that provides project-level instructions to an AI coding agent.
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

## References

Do not load all references at once. Read the relevant reference when you need it.

| When... | Read | Environment |
|---------|------|-------------|
| Helping user identify what type of skill to build | `references/skill-categories.md` | All |
| User needs config setup, memory, hooks, or composable scripts | `references/advanced-patterns.md` | All (hooks: Claude Code only) |
| Running formal evals with subagents | `references/full-eval.md` | Claude Code / Cowork only |
| Running tests without subagents | `references/quick-test.md` | Claude.ai only |
| Optimizing description for triggering accuracy | `references/description-optimization.md` | Claude Code / Cowork only |
| User wants to improve an agent context file, or a skill is overkill | `references/claude-md-guide.md` | Claude Code (CLAUDE.md / AGENTS.md); Claude.ai (project instructions) |
| Need JSON schemas for evals, grading, benchmark, etc. | `references/schemas.md` | All |

---

## Read the Situation First

Before doing anything, assess what the user actually needs. This is the most important step — it determines everything else.

**Read these signals:**

- **User already has a draft?** → Skip the wizard. Go straight to review/diagnose mode (Path 4).
- **User says "turn this into a skill"?** → Use conversation extraction (Path 3).
- **Request is trivially simple?** (e.g., "just add a signature to my emails") → Don't force 8 wizard steps. Generate a minimal skill immediately. Match the skill's complexity to the task's complexity — a 1-line behavior gets a 10-line skill, not a 150-line monstrosity. **For simple requests, skip headers and explanatory preamble — just produce the SKILL.md.**
- **User provided enough detail?** → Build immediately. If the prompt contains the workflow, format preferences, constraints, and output shape, that's enough — produce the full SKILL.md in the first response. Do not start a wizard interview when the user has already given you everything you need. Clarifying questions (if any) go alongside the draft, not instead of it.
- **Request is complex with many steps?** → Full wizard flow. Take your time on edge cases and scripts.
- **Request is vague?** (e.g., "help me set up stuff faster") → Use the wizard to draw out specifics. Don't generate anything until you understand the actual workflow.
- **User is frustrated with a broken skill?** → Don't re-ask questions they already answered. Acknowledge the problem, diagnose directly, and fix it.
- **Requirements contradict each other?** → Surface the tension explicitly before generating — do not paper over it. Name the contradiction, explain why it matters (inconsistent output), and offer concrete resolution paths: two output modes (quick vs. detailed), layered output (TL;DR + full version), or two separate skills. A skill built on contradictions will produce inconsistent output every time. Do not build it — resolve the contradiction first.
- **Request overlaps with something Claude already does well?** → You must directly address this. Say out loud: "Claude already handles [this task] reasonably well without a skill." Then probe: "What specifically is missing — a particular format, structure, or workflow?" If the user can articulate specifics (a rigid output format, a multi-step process, a house style), build the skill. If the user has no concrete additions beyond the baseline task, tell them directly: "A skill here would add overhead without improving output — you'd get the same result by just asking Claude." Do not sidestep this by generating a skill anyway.
- **User's issue is better solved by an agent context file than a skill?** → If the problem is "Claude keeps ignoring my project conventions" (testing patterns, API conventions, code style), **do not create a skill**. Tell the user directly that a skill is the wrong tool here, explain why (skills are for workflows, agent context files like CLAUDE.md or AGENTS.md are for project-level conventions), and help them fix their agent context file instead. Read `references/claude-md-guide.md` for the `<important if>` pattern and writing principles for CLAUDE.md, AGENTS.md, and `.cursorrules`. Offering to build a skill anyway in this situation is a mistake.

**Scale your response to the task:**
- Trivial tasks → minimal skill, fast turnaround, no headers or preamble
- Clear/detailed tasks → produce the artifact immediately; ask questions alongside the draft if needed
- Complex tasks → full wizard, edge cases, scripts architecture, test cases
- Vague tasks → discovery questions first, skill later

**The default is to build, not to plan.** When in doubt, produce a draft. Users can react to a concrete draft far better than to a list of questions. "I drafted this based on what you said — does it land?" is almost always better than "Before I start, let me ask you 5 questions."

**When producing a skill, output the actual file — not a description of it.** The output must be the SKILL.md content in a fenced code block. Not "here's what I'd put in each section." Not a bulleted outline. Not "Step 1 would cover X, Step 2 would cover Y." The file itself, in full. If you catch yourself writing "The SKILL.md would include..." — stop. Write the SKILL.md instead.

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

**Watch for contradictions** when restating. If requirements pull in opposite directions (e.g., "thorough but concise", "comprehensive but short"), stop and surface the tension explicitly — don't paper over it with a clever pattern like "progressive disclosure." Name the contradiction: "These two requirements pull in opposite directions. A skill built on both will produce inconsistent output every run." Then offer concrete resolution paths: two output modes in one skill (triggered by a keyword like "quick" vs. "full"), layered output (TL;DR + detail below a fold), or two separate skills. Get agreement before generating anything.

**Watch for overlap** with Claude's built-in abilities. If the task is something Claude already does well by default (summarizing, translating, basic code review, email drafting), probe for what the skill adds: "Claude already handles [task] pretty well out of the box. What's missing — a specific format, style, or process you want locked in?" If the user has specific requirements, the skill is justified. If not, gently explain it would add overhead without improving output.

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
Proactively ask about edge cases, input/output formats, example files, success criteria, and dependencies. Check available MCPs for research if useful. Wait to write test prompts until you've ironed this part out.

**Step 7 — Pick a starting point**
Based on what you've learned, check if one of the built-in templates (see `templates/` directory) is a close fit. If so, offer it: "This sounds like a [content writer / document generator / verification skill / runbook]. I have a starter template for that — want me to use it as a base, or start from scratch?"

Also read `references/skill-categories.md` to identify which of the 9 skill categories this fits (library reference, product verification, data analysis, business process, scaffolding, code quality, CI/CD, runbook, or infrastructure operations). Knowing the category helps you write better instructions because each has different best practices.

If no template fits, start from a blank SKILL.md.

**Step 8 — Generate the draft**
Write the SKILL.md based on everything gathered. Show it to the user and explain each section briefly in plain language. Ask: "How does this look? Anything you'd change?"

**Produce the full file, not a plan.** The output of this step is the actual SKILL.md content in a markdown code block — not a summary of what the file will contain, not a list of sections to fill in later, not "here's what I'd put in each section." If you've done steps 1–7, you have enough information to generate the full draft.

Domain-specific depth is required — generic placeholders are not useful:
- **Runbooks:** Include the actual symptom routing table (symptom → likely cause → investigation path), real log query patterns for the user's tooling (Datadog, CloudWatch, Splunk, etc.) with correct syntax and filter examples, specific dashboard names/URLs if known (use clearly-labeled placeholders like `[YOUR_GRAFANA_DASHBOARD_URL]` for things only the user knows), and a structured findings report template with named fields (severity, timeline, root cause, impact, follow-up actions).
- **Verification skills:** Include the actual assertion logic in `scripts/` with real code, not pseudocode. Step-by-step assertions at each checkpoint, not just the final state.
- **Data processing skills:** Include real script code with actual library calls, field mappings, and error handling — not skeleton functions.

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
| Verification | `templates/verification.md` | End-to-end testing and verification of features, flows, or integrations |
| Scaffolding | `templates/scaffolding.md` | Generating boilerplate for new components, services, or projects |
| Runbook | `templates/runbook.md` | Incident investigation: symptom → diagnosis → structured findings report |

When presenting templates, describe them by what they help the user accomplish, not by their internal structure. For example: "I have a Content Writer template that's great for keeping a consistent voice across blog posts and social media. Want me to customize it for you?"

After selecting a template, walk through the customization: fill in their specific voice, format preferences, examples, and constraints. The template provides the skeleton; the user provides the soul.

**Skill categories:** Skills cluster into 9 recurring categories. Knowing which type helps write better instructions because each has different best practices. Read `references/skill-categories.md` for the full taxonomy with examples. The categories are: library & API reference, product verification, data fetching & analysis, business process automation, code scaffolding, code quality & review, CI/CD & deployment, runbooks, and infrastructure operations.

**MCP-enhanced skills:** Some skills add a guidance layer on top of Claude's existing MCP connections (Notion, Linear, Figma, etc.). The skill doesn't give Claude new tools — it teaches Claude *how to use existing tools for a specific workflow*. When building these: reference specific MCP tool capabilities in the instructions, include tool-specific patterns, handle MCP unavailability gracefully (tell the user the connection is needed), and be aware of rate limits when making many API calls.

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

**Do NOT re-run the wizard.** The user already has something — they want diagnosis, not a restart. Do NOT ask what the skill is supposed to do — read it and figure that out yourself.

**How to review an existing skill:**

1. **Read the SKILL.md carefully.** Before running any tests, look for common problems:
   - **Thin description** — fewer than 3 trigger phrases almost guarantees undertriggering
   - **Vague instructions** — phrases like "be thorough but not nitpicky" or "use good judgment" produce inconsistent output because Claude interprets them differently each run
   - **Missing output format example** — abstract descriptions of format ("a numbered list with severity") vary across runs; concrete examples lock it in
   - **No edge case handling** — the skill works for the happy path but fails on unusual inputs
   - **Overly broad triggering** — description matches too many contexts (e.g., "writes professional content" triggers on emails when it should only trigger on LinkedIn posts)
   - **Missing gotchas section** — no record of common failure points (see writing principles below)
   - **Stating the obvious** — restating what Claude already knows instead of focusing on what pushes it out of default behavior

2. **Diagnose and rank problems.** Tell the user what you found, ordered from most impactful to least. Be specific: "Your description says 'Reviews code' — that's 2 words. A developer saying 'check my Python script for performance issues' might not trigger this because the description doesn't mention Python, performance, or scripts."

3. **Propose fixes with reasoning.** Don't just rewrite — explain why each change matters. The user learns to write better skills, and they can push back if they disagree with the reasoning.

4. **Preserve the user's intent and structure.** Improve the skill, don't rebuild it from scratch. The user has context about their workflow that you don't — respect it. Do not introduce new external dependencies (new reference files, new scripts) unless the user asks for them.

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

A skill is a folder, not just a markdown file. Think of the entire file system as a form of context engineering and progressive disclosure. Tell Claude what files are in your skill, and it will read them at appropriate times.

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

The description is not a summary — it's a trigger specification. Claude scans it to decide "is there a skill for this request?" Write it to answer that question, not to describe the skill to a human reader.

Claude currently has a tendency to "undertrigger" — to not use skills when they'd be useful. To combat this, make descriptions a little "pushy." Include specific phrases users would say, and err on the side of triggering too much rather than too little.

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

## Gotchas
Common failure points and how to handle them. Build this from real failures
and update it over time as new edge cases surface.

## Common Pitfalls
Things that tend to go wrong and how to handle them.
```

**Key writing principles:**

- **Don't state the obvious.** Claude already knows a lot about coding and has default opinions. If a skill is primarily about knowledge, focus on information that pushes Claude out of its normal way of thinking — gotchas, internal conventions, non-obvious patterns, and things it gets wrong. Restating what Claude already knows wastes context and dilutes the signal from the instructions that actually matter.

- **Build a gotchas section.** The highest-signal content in any skill is a gotchas section. These capture common failure points that Claude runs into when using the skill. Build them from real failures and update them over time as new edge cases surface. This is the section that makes the difference between a skill that works on paper and one that works in practice.

- **Give Claude flexibility (avoid railroading).** Claude will generally try to stick to your instructions, and because skills are reusable you want to be careful of being too specific. Give Claude the information it needs (context, constraints, examples) but give it the flexibility to adapt to the situation. Specify *what* and *why*, not every detail of *how*. If you find yourself writing rigid step-by-step instructions for something Claude could figure out from context, you're probably railroading.

- **Explain the why.** Instead of "ALWAYS use bullet points", write "Use bullet points for lists of 3+ items because the reader will scan these sections quickly and bullets improve readability." Try to explain why things are important rather than using heavy-handed MUSTs. Today's LLMs are smart — they have good theory of mind and when given a good harness can go beyond rote instructions.

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

This separation is the difference between a skill that's reliable across hundreds of runs and one that subtly varies each time.

**Write functional scripts, not stubs.** When the skill includes a `scripts/` folder, the scripts must contain actual working logic — not comments like `# TODO: add parsing logic here` or placeholder skeleton functions. If the user needs OCR, include the `pytesseract` / `pdf2image` import and the actual extraction call. If they need CSV parsing, use `csv` or `pdfplumber` with real field mapping. Skeleton stubs are not useful. If you are uncertain about a specific implementation detail (e.g., the exact PDF format), make a reasonable assumption, note it in a comment, and implement the rest fully. A partial implementation with one noted assumption is far better than an empty stub.

Before calling a script done, mentally verify:
- Every import is real (not invented) and the library can do what you're using it for
- The main logic path runs end-to-end without hitting a `pass`, `TODO`, or `raise NotImplementedError`
- Data flows correctly between steps (e.g., if step 1 returns a list of dicts, step 2 actually iterates that list — not a placeholder variable)
- OCR: uses `pdf2image` + `pytesseract` (not just `pdfplumber` text extraction, which silently returns empty strings on image-based PDFs)
- Math operations use the actual computed values, not hardcoded test numbers

**Handle error cases in scripts.** If the prompt mentions "using OCR if needed" or "rock solid" or "don't make me reinvent the wheel", that's a signal the user expects resilience — include try/except blocks, fallback logic, and meaningful error messages.

Beyond single-purpose scripts, consider providing **composable helper libraries** — reusable functions that Claude can import and combine to build more complex workflows on the fly. For example, a data analysis skill might include helper functions for fetching events, computing funnels, and flagging anomalies. Claude can then compose these into custom scripts for specific queries. Read `references/advanced-patterns.md` for detailed examples.

Design scripts with CLI interfaces (`--input`, `--output`, `--help` flags) so they're reusable and testable independently of the skill.

Use **references** for large bodies of knowledge that the skill needs sometimes but not always. Point to them from SKILL.md with clear guidance on when to read them.

Use **assets** for files that get embedded in output (templates, images, fonts, icons).

For advanced patterns including config/setup files, persistent memory/data storage, and on-demand hooks, read `references/advanced-patterns.md`.

**Memory requirement signal:** If the user's request includes words like "remember", "last time", "history", "track over time", or "knows what it posted before", the skill needs persistent storage. Do not implement this as a vague suggestion — mandate `${CLAUDE_PLUGIN_DATA}` as the storage location in the SKILL.md instructions. Data stored in the skill directory itself may be deleted on upgrade; `${CLAUDE_PLUGIN_DATA}` survives upgrades. Read `references/advanced-patterns.md` for the exact implementation pattern.

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

### Running Tests

Choose the testing approach based on your environment:

- **Claude Code / Cowork (subagents available):** Read `references/full-eval.md` for the full parallel eval workflow with baselines, grading, benchmarking, and the eval viewer.
- **Claude.ai (no subagents):** Read `references/quick-test.md` for the simplified workflow.

**Common fixes during iteration:**
- Skill doesn't trigger → improve the description (add more trigger phrases, be pushier)
- Output format is wrong → add more specific format instructions or an example
- Missing steps → add them, with reasoning for why they matter
- Tone is off → add voice/style examples with both good and bad examples

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
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration (if using the eval viewer)
4. Wait for user review
5. Read feedback, improve, repeat

Keep going until the user is happy, feedback is all empty, or you're not making meaningful progress.

---

## Description Optimization

After the skill is working well, offer to optimize the description for better triggering accuracy. Read `references/description-optimization.md` for the full 4-step process (generating eval queries, reviewing with the user, running the optimization loop, and applying results).

Note: The automated optimization loop requires `claude -p` and is only available in Claude Code and Cowork. On Claude.ai, manually iterate on the description based on user feedback.

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
- **Team use:** Admins can deploy skills across an entire workspace so all team members get the same skill behavior automatically. When building skills for teams, prioritize consistency: use rigid output frameworks (not "use your judgment"), embed team-specific references directly (don't leave "[add your principles here]" placeholders), and make the structure explicit enough that output from any team member is comparable.
- **Claude Code:** Place the folder in your skills directory, or distribute as a plugin via the marketplace.
- **Public sharing:** Host the skill folder on GitHub with a clear README explaining what it does, how to install it, and what it looks like in action.

### Distribution at Scale

For smaller teams, checking skills into repos (under `.claude/skills/`) works well. But every checked-in skill adds to Claude's context. As you scale, consider an internal plugin marketplace where users install only what they need.

**Organic curation:** Don't centrally decide which skills are valuable. Let people upload skills to a sandbox or shared folder, promote them in Slack, and graduate to the marketplace once they've gotten traction. Some curation before official release prevents redundancy.

**Composing skills:** Skills can reference other skills by name — Claude will invoke them if installed. Treat these as optional enhancements, not hard dependencies.

**Measuring usage:** Use a PreToolUse hook to log skill invocations — helps identify popular skills and catch undertriggering.

---

## Quick Reference: The Core Loop

1. **Understand** — What does the user want? (wizard interview, template selection, or conversation extraction)
2. **Draft** — Write the SKILL.md with proper frontmatter, clear instructions, and examples
3. **Test** — Run 2-3 realistic prompts through the skill
4. **Review** — Show results to the user, get feedback
5. **Improve** — Update the skill based on feedback, generalizing rather than overfitting
6. **Repeat** — Until the user is happy
7. **Optimize** — Fine-tune the description for reliable triggering
8. **Package** — Bundle, present, and share

Please add steps to your TodoList if you have one. If you're in Cowork, specifically add "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" to make sure it happens.
