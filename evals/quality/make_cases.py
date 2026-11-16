"""Writes one case folder (case.yaml) per quality case for `claude plugin eval`. Edit the JSON files, rerun.
Sources: write-prose.json (inputs inlined from inputs/), write-readme.json (fixture repos, written by a scaffold script)
and improve-codebase.json (fixture repos with a commit history, from fixtures/; see fixture_repo.py and score.py).
case.yaml is written as JSON, which YAML accepts."""
import json, pathlib, shutil

import fixture_repo

here = pathlib.Path(__file__).parent
JUDGE_NOTE = "Judge only the claim above, against the task below. Pass when it clearly holds; fail when it doesn't."

def criteria_list(expectations, default_focus, task):
    out = []
    for i, e in enumerate(expectations, 1):
        crit, focus = (e["criteria"], e["focus"]) if isinstance(e, dict) else (e, default_focus)
        out.append({"type": "llm", "name": f"check-{i:02d}", "criteria": f"Claim: {crit}\n\n{JUDGE_NOTE}\n\n<task>\n{task}\n</task>", "focus": focus})
    return out

def loads(skill):
    return {"type": "tool_used", "name": "loads-skill", "tool": "Skill",
            "input_match": r'"skill"\s*:\s*"(?:[\w-]+:)?' + skill + '"', "min": 1}

def heredocs(files):
    lines = ["set -e"]
    for path, body in files.items():
        if "/" in path:
            lines.append(f"mkdir -p '{path.rsplit('/', 1)[0]}'")
        lines.append(f"cat > '{path}' <<'FIXTURE_EOF'\n{body.rstrip(chr(10))}\nFIXTURE_EOF")
    return "\n".join(lines) + "\n"

def write_case(cid, skill, prompt, graders, tools, turns, timeout, scaffold=None):
    d = here / cid
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    case = {
        "schema_version": "1.1",
        "name": f"quality-{cid}",
        "tags": ["quality", skill, f"quality-{skill}"],
        "plugins": ["../../.."],
        "runs": 1,
        "execution": {"prompt": prompt, "max_turns": turns, "timeout_seconds": timeout, "allowed_tools": tools},
        "graders": [loads(skill)] + graders,
    }
    if scaffold:
        (d / "scaffold.sh").write_text(scaffold)
        case["context"] = {"scaffold_script": "scaffold.sh"}
    (d / "case.yaml").write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")

def fixture_task(c):
    files = "\n\n".join(f"--- {path} ---\n{body}" for path, body in c["fixture"].items())
    return f"{c['prompt']}\n\nThe repository before the run:\n\n{files}"

ids = []
for c in json.loads((here / "write-prose.json").read_text()):
    prompt = c["prompt"]
    for name in c["input"]:
        prompt += "\n\n" + (here / "inputs" / name).read_text()
    write_case(c["id"], "write-prose", prompt, criteria_list(c["expectations"], "last_message", prompt),
               ["Read", "Glob", "Grep", "Skill"], 8, 400)
    ids.append(c["id"])

for c in json.loads((here / "write-readme.json").read_text()):
    write_case(c["id"], "write-readme", c["prompt"],
               criteria_list(c["expectations"], {"source": "file", "path": "README.md"}, fixture_task(c)),
               ["Read", "Glob", "Grep", "Skill", "Write", "Edit", "Bash"], 30, 900, heredocs(c["fixture"]))
    ids.append(c["id"])

# improve-codebase: the judge checks the final report here; behavior and structure are measured afterwards by score.py
for c in json.loads((here / "improve-codebase.json").read_text()):
    task = f"{c['prompt']}\n\nAbout the repository (the agent was not told this):\n{fixture_repo.checks(c['fixture'])['facts']}"
    write_case(c["id"], "improve-codebase", c["prompt"], criteria_list(c["expectations"], "last_message", task),
               ["Read", "Glob", "Grep", "Skill", "Write", "Edit", "Bash"], 150, 2700, fixture_repo.scaffold(c["fixture"]))
    ids.append(c["id"])

(here / "cases.txt").write_text("\n".join(ids) + "\n")
print(f"{len(ids)} quality cases written")
