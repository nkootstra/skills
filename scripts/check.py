"""Structural checks for the repo. Runs in CI; run it locally before pushing.
usage: python3 scripts/check.py"""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []
def fail(msg): errors.append(msg)

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None

def field(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None

# marketplace: every skill in exactly one plugin
market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
owner = {}
for plugin in market["plugins"]:
    name = plugin.get("name", "?")
    for key in ("name", "version", "author"):
        if key not in plugin:
            fail(f"marketplace: plugin {name} has no {key}")
    if not SEMVER.match(plugin.get("version", "")):
        fail(f"marketplace: plugin {name} version {plugin.get('version')!r} is not semver")
    for path in plugin.get("skills", []):
        skill = path.removeprefix("./")
        if not (root / skill / "SKILL.md").is_file():
            fail(f"marketplace: {name} lists {path}, which has no SKILL.md")
        if skill in owner:
            fail(f"marketplace: {skill} is listed in both {owner[skill]} and {name}")
        owner[skill] = name
for md in sorted(root.glob("skills/*/SKILL.md")):
    skill = str(md.parent.relative_to(root))
    if skill not in owner:
        fail(f"marketplace: {skill} is not listed in any plugin")

# each SKILL.md
skill_names = []
for md in sorted(root.glob("skills/*/SKILL.md")):
    folder = md.parent.name
    text = md.read_text()
    fm = frontmatter(text)
    if fm is None:
        fail(f"{folder}: SKILL.md has no frontmatter"); continue
    skill_names.append(folder)
    if field(fm, "name") != folder:
        fail(f"{folder}: name is {field(fm, 'name')!r}, expected the folder name")
    desc = field(fm, "description") or ""
    if not desc:
        fail(f"{folder}: description is missing")
    elif len(desc) > 1024:
        fail(f"{folder}: description is {len(desc)} characters, the limit is 1024")
    meta = re.search(r"^metadata:\n((?:[ \t]+.+\n?)+)", fm + "\n", re.M)
    block = meta.group(1) if meta else ""
    if not re.search(r"^\s+author:\s*Niels Kootstra\s*$", block, re.M):
        fail(f"{folder}: metadata.author must be Niels Kootstra")
    if not re.search(r'^\s+version:\s*"\d+\.\d+\.\d+"\s*$', block, re.M):
        fail(f'{folder}: metadata.version must be a quoted semver, e.g. "1.0.0"')
    lines = len(text.splitlines())
    if lines >= 500:
        fail(f"{folder}: SKILL.md is {lines} lines, keep it under 500")
    linked = set(re.findall(r"\]\(([^)#:\s]+\.md)\)", re.sub(r"`[^`]*`", "", text)))
    for stray in sorted(p.name for p in md.parent.glob("*.md") if p.name != "SKILL.md"):
        fail(f"{folder}: {stray} belongs in references/")
    for ref in sorted(p.name for p in (md.parent / "references").glob("*.md")):
        if f"references/{ref}" not in linked:
            fail(f"{folder}: references/{ref} is not linked from SKILL.md")

# relative links resolve (inline code and fenced blocks ignored)
docs = list(root.glob("skills/*/*.md")) + list(root.glob("skills/*/references/*.md")) + [root / "README.md", root / "AGENTS.md"]
for doc in docs:
    text = re.sub(r"```.*?```", "", doc.read_text(), flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"^[a-z]+:|^#", target):
            continue
        path = target.split("#")[0]
        if not (doc.parent / path).exists():
            fail(f"{doc.relative_to(root)}: broken link {target}")

# eval cases: generated folders are gitignored, so check the sources instead
import importlib.util, subprocess, sys, tempfile
trig = root / "evals/triggering"
spec = importlib.util.spec_from_file_location("trigger_cases", trig / "make_cases.py")
trigger = importlib.util.module_from_spec(spec); spec.loader.exec_module(trigger)
cases = trigger.CASES
ids = [c[0] for c in cases]
for dup in sorted({i for i in ids if ids.count(i) > 1}):
    fail(f"evals: triggering case id {dup} is used twice")
for cid, exp, ok, diff, prompt in cases:
    for name in [exp] + list(ok):
        if name != "none" and name not in skill_names:
            fail(f"evals: triggering case {cid} names {name}, which is not a skill")
for name in skill_names:
    positives = sum(1 for c in cases if c[1] == name)
    if positives < 8:
        fail(f"evals: {name} has {positives} positive triggering cases, it needs 8")
if (trig / "cases.md").read_text() != trigger.cases_md():
    fail("evals: evals/triggering/cases.md is out of date; rerun python3 evals/triggering/make_cases.py")
for script in ("make_cases.py", "summarize.py"):
    m = re.search(r"^SKILLS\s*=\s*\[(.*?)\]", (trig / script).read_text(), re.M | re.S)
    listed = set(re.findall(r'"([\w-]+)"', m.group(1))) if m else set()
    for name in skill_names:
        if name not in listed:
            fail(f"evals: {name} is missing from SKILLS in evals/triggering/{script}")

# both generators still run (into a temp folder, so the check writes nothing in the repo)
with tempfile.TemporaryDirectory() as tmp:
    for script in ("evals/triggering/make_cases.py", "evals/quality/make_cases.py"):
        out = pathlib.Path(tmp) / script.split("/")[1]
        r = subprocess.run([sys.executable, str(root / script), "--out", str(out)], capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"evals: {script} fails: {(r.stderr or r.stdout).strip().splitlines()[-1]}")

# release workflow offers every plugin
release = (root / ".github/workflows/release.yml").read_text()
m = re.search(r"plugin:.*?options:\s*\[(.*?)\]", release, re.S)
options = {o.strip() for o in m.group(1).split(",")} if m else set()
for plugin in market["plugins"]:
    if plugin["name"] not in options:
        fail(f"release.yml: plugin {plugin['name']} is not an option of the plugin input")

if errors:
    print("\n".join(f"✗ {e}" for e in errors))
    sys.exit(1)
print(f"✓ {len(skill_names)} skills, {len(market['plugins'])} plugin(s), {len(cases)} eval cases")
