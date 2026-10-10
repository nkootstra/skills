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

# triggering eval is in sync
trig = root / "evals/triggering"
cases = [json.loads(l) for l in (trig / "cases.jsonl").read_text().splitlines() if l.strip()]
ids = {c["id"] for c in cases}
dirs = {p.name for p in trig.iterdir() if (p / "prompt.md").is_file()}
if ids != dirs:
    fail(f"evals: case folders differ from cases.jsonl (missing {sorted(ids - dirs)}, extra {sorted(dirs - ids)}); "
         "rerun python3 evals/triggering/make_cases.py")
for script in ("make_cases.py", "summarize.py"):
    m = re.search(r"^SKILLS\s*=\s*\[(.*?)\]", (trig / script).read_text(), re.M | re.S)
    listed = set(re.findall(r'"([\w-]+)"', m.group(1))) if m else set()
    for name in skill_names:
        if name not in listed:
            fail(f"evals: {name} is missing from SKILLS in evals/triggering/{script}")

qual = root / "evals/quality"
qids = set((qual / "cases.txt").read_text().split())
qdirs = {p.name for p in qual.iterdir() if (p / "case.yaml").is_file()}
if qids != qdirs:
    fail(f"evals: quality case folders differ from cases.txt (missing {sorted(qids - qdirs)}, extra {sorted(qdirs - qids)}); "
         "rerun python3 evals/quality/make_cases.py")

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
