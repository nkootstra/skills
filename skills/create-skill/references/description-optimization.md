# Description Optimization

> **Environment:** This reference applies to Claude Code and Cowork only. The optimization loop requires the `claude` CLI tool (`claude -p`), which is not available on Claude.ai. On Claude.ai, manually iterate on the description based on user feedback instead.

After the skill is working well, optimize the description for better triggering accuracy.

## How Skill Triggering Works

Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. Important: Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means eval queries should be substantive enough that Claude would actually benefit from consulting the skill. Simple queries like "read file X" are poor test cases.

## Step 1: Generate Trigger Eval Queries

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

## Step 2: Review with User

Present the eval set for review using the HTML template:
1. Read the template from `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array, `__SKILL_NAME_PLACEHOLDER__` with the name, `__SKILL_DESCRIPTION_PLACEHOLDER__` with the description
3. Write to a temp file and open it
4. User edits, then clicks "Export Eval Set"
5. Check Downloads folder for the JSON

This step matters — bad eval queries lead to bad descriptions.

## Step 3: Run the Optimization Loop

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

## Step 4: Apply the Result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.
