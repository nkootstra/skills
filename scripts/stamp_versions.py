"""Stamps release versions: the plugin in marketplace.json, and each of its skills that changed since the last release.
usage: python3 scripts/stamp_versions.py <plugin> <patch|minor|major> <last-tag or ""> [--dry-run]
Prints the new version on the first line, then one changed file per line. Used by .github/workflows/release.yml."""
import json, pathlib, re, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if a != "--dry-run"]
dry = "--dry-run" in sys.argv
if len(args) != 3 or args[1] not in ("patch", "minor", "major"):
    sys.exit(__doc__)
plugin_name, part, last_tag = args

def bump(version, part):
    major, minor, patch = map(int, version.split("."))
    if part == "major": return f"{major + 1}.0.0"
    if part == "minor": return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"

market_path = root / ".claude-plugin/marketplace.json"
market = json.loads(market_path.read_text())
plugin = next((p for p in market["plugins"] if p["name"] == plugin_name), None)
if plugin is None:
    sys.exit(f"no plugin named {plugin_name} in marketplace.json")

# First release: ship the version already on main; nothing to stamp.
if not last_tag:
    print(plugin["version"])
    sys.exit(0)

released = last_tag.rsplit("-v", 1)[1]
next_version = bump(released, part)
changed_files = [market_path]
plugin["version"] = next_version

for path in plugin["skills"]:
    skill = path.removeprefix("./")
    existed = subprocess.run(["git", "cat-file", "-e", f"{last_tag}:{skill}/SKILL.md"],
                             cwd=root, capture_output=True).returncode == 0
    unchanged = subprocess.run(["git", "diff", "--quiet", last_tag, "HEAD", "--", skill], cwd=root).returncode == 0
    if not existed or unchanged:
        continue  # new skills keep the version they were written with
    md = root / skill / "SKILL.md"
    text = md.read_text()
    pattern = re.compile(r'(^metadata:\n(?:[ \t]+.+\n)*?[ \t]+version:\s*")(\d+\.\d+\.\d+)(")', re.M)
    m = pattern.search(text)
    if not m:
        sys.exit(f"{md}: no metadata.version to stamp")
    text = text[:m.start(2)] + bump(m.group(2), part) + text[m.end(2):]
    if not dry:
        md.write_text(text)
    changed_files.append(md)

if not dry:
    market_path.write_text(json.dumps(market, indent=2, ensure_ascii=False) + "\n")
print(next_version)
for f in changed_files:
    print(f.relative_to(root))
