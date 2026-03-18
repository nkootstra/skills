# Full Eval (Claude Code / Subagent Environments)

> **Environment:** This reference applies to Claude Code and Cowork only. These environments have subagents, which are required for the parallel eval workflow described here. If you're on Claude.ai (no subagents), read `references/quick-test.md` instead.

This is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

## Step 1: Spawn All Runs in the Same Turn

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

## Step 2: While Runs Are in Progress, Draft Assertions

Don't just wait — use this time to draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable and have descriptive names that read clearly in the benchmark viewer.

Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with assertions once drafted. Explain to the user what they'll see in the viewer.

## Step 3: As Runs Complete, Capture Timing Data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory — this is the only opportunity to capture it. It comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## Step 4: Grade, Aggregate, and Launch the Viewer

Once all runs are done:

1. **Grade each run** — spawn a grader subagent (or grade inline) that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names. For assertions that can be checked programmatically, write and run a script rather than eyeballing it.

2. **Aggregate into benchmark:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <n>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean +/- stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects. Put each with_skill version before its baseline counterpart.

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

## Step 5: Read the Feedback

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

## What the User Sees in the Viewer

The "Outputs" tab shows one test case at a time: the prompt, the files the skill produced (rendered inline where possible), formal grades if grading was run, a feedback textbox, and previous feedback from earlier iterations. Navigation is via prev/next buttons or arrow keys.

The "Benchmark" tab shows stats: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

When done, the user clicks "Submit All Reviews" which saves all feedback to `feedback.json`.

## Cowork-Specific Adaptations

If you're in Cowork:

- You have subagents, so the main workflow works (spawn in parallel, run baselines, grade, etc.). If timeouts are a problem, run test prompts in series.
- No browser/display — use `--static <output_path>` for the eval viewer to write a standalone HTML file. The user can open it in their browser.
- The "Submit All Reviews" button downloads `feedback.json` as a file. Read it from the Downloads folder (you may need to request access).
- Packaging works — `package_skill.py` needs Python and a filesystem.
- Description optimization (`run_loop.py` / `run_eval.py`) works since it uses `claude -p` via subprocess.
- Save description optimization until the skill is fully finished and the user agrees it's in good shape.

## Advanced: Blind Comparison

For situations where you want rigorous comparison between two skill versions ("is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for details. The idea: give two outputs to an independent agent without revealing which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.
