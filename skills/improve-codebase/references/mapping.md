# Mapping a codebase

The map has four parts: what is there, what depends on what, what changes, and what changes together. Collect all four before reading any file closely; they decide which files deserve the close read.

Every command below runs from the repo root and only reads files and git history. `git grep` searches tracked files only, which keeps untracked build output out but not lockfiles, `vendor/` or generated code that is committed. Add pathspec excludes for those, such as `':!*.lock' ':!*lock.json' ':!*.lockb' ':!vendor/' ':!*.min.js' ':!*.snap'`, and the repo's own generated folders. The patterns use POSIX classes (`[[:space:]]`) because `\s` and `\b` don't work in `git grep -E` on every platform. Save the scripts outside the repo, or delete them before committing.

## Contents

- [What is there](#what-is-there)
- [What depends on what](#what-depends-on-what)
- [What changes](#what-changes)
- [What changes together](#what-changes-together)
- [Markers worth counting](#markers-worth-counting)
- [Reading the map](#reading-the-map)

## What is there

Files by size, largest first:

```sh
git ls-files -z -- ':!*.lock' ':!*lock.json' ':!*.lockb' ':!vendor/' ':!*.min.js' ':!*.snap' | xargs -0 wc -l 2>/dev/null | grep -v ' total$' | sort -rn | head -30
```

A skeleton: every declaration with its file and line, without bodies. Narrow the pathspecs to the languages in the repo. It covers functions and types in TS/JS, Python, Go and Rust, and types only in Java, C# and Kotlin, whose methods have no keyword to match.

```sh
git grep -nE '^[[:space:]]*((export|default|pub(\([^)]*\))?|public|private|protected|internal|static|abstract|async|final|open|override)[[:space:]]+)*(function|class|interface|type|enum|def|fn|struct|trait|impl(<[^>]*>)?|record|object)[[:space:]]+[A-Za-z_]|^[[:space:]]*func[[:space:]]+(\([^)]*\)[[:space:]]+)?[A-Za-z_]|^[[:space:]]*export[[:space:]]+const[[:space:]]+[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=[[:space:]]*(async[[:space:]]*)?\(' -- '*.ts' '*.tsx' '*.js' '*.py' '*.go' '*.rs' '*.java' '*.cs' '*.kt'
```

For a repo too large to hold at once, split by top-level folder and give each to a subagent with one instruction: return the public surface, what the area imports from other areas, and anything that surprised you, in under 40 lines. Reason across the summaries, then read the code only where the map points.

## What depends on what

Use the language's own tool when the project has one, because it resolves aliases and package names:

| Stack | Command |
|---|---|
| JS/TS | `npx madge --circular --extensions ts,tsx src` for cycles, when the project already uses madge or dependency-cruiser |
| Go | `go list -f '{{.ImportPath}}: {{join .Imports " "}}' ./...` prints each package's imports; the compiler rejects cycles, so look at direction instead |
| Rust | `cargo tree` for the edges between crates |

Don't add a dependency to the project to draw the graph.

When no tool is set up, this script gives the edges between areas of a JS/TS or Python tree from relative imports alone. It misses path aliases and absolute package imports, so treat a missing edge as unknown, not as absent.

```python
"""Relative-import edges between the areas of a JS/TS or Python source tree, with cycles marked.
usage: python3 edges.py <source root> [depth]   e.g. python3 edges.py src 1"""
import collections, os, re, sys

root = os.path.normpath(sys.argv[1] if len(sys.argv) > 1 else ".")
depth = int(sys.argv[2]) if len(sys.argv) > 2 else 1
SKIP = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv", "venv"}
JS = re.compile(r"""(?:\bfrom|\bimport|\brequire\()\s*['"](\.{1,2}/[^'"]+)['"]""")
PY = re.compile(r"^\s*from\s+(\.+)([\w.]*)\s+import", re.M)

def area(path):
    parts = os.path.relpath(path, root).split(os.sep)
    return "/".join(parts[:depth]) if len(parts) > depth else "(root)"

edges = collections.Counter()
tree = []
for folder, dirs, names in os.walk(root):
    dirs[:] = [d for d in dirs if d not in SKIP]
    tree.append((folder, names))
folders = {os.path.normpath(folder) for folder, _ in tree}   # exact names: isdir() ignores case on some filesystems
for folder, names in tree:
    for name in names:
        if not name.endswith((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py")):
            continue
        path = os.path.join(folder, name)
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        targets = [m.group(1) for m in JS.finditer(text)]
        targets += ["../" * (len(m.group(1)) - 1) + m.group(2).replace(".", "/") for m in PY.finditer(text)]
        for rel in targets:
            target = os.path.normpath(os.path.join(folder, rel))
            if os.path.relpath(target, root).startswith(".."):
                continue
            a, b = area(path), area(os.path.join(target, "index") if target in folders else target)
            if a != b:
                edges[(a, b)] += 1
for (a, b), n in sorted(edges.items(), key=lambda e: (-e[1], e[0])):
    back = edges.get((b, a), 0)
    print(f"{n:>4}  {a} -> {b}" + (f"   cycle: {back} back" if back else ""))
```

Output is one line per edge, heaviest first: `24  blocks -> data   cycle: 1 back`. Rerun it after each batch of changes; the edge count between two areas is one of the numbers the report compares.

## What changes

Commits per file over the last year:

```sh
git log --since="12 months ago" --no-merges --name-only --format= | grep -v '^$' | grep -Fx -f <(git ls-files) | sort | uniq -c | sort -rn | head -30
```

The `grep -Fx` keeps only files that still exist (it needs bash or zsh). The same, limited to commits whose message reads like a repair. A file high on both lists is where the structure is producing bugs.

```sh
git log --since="12 months ago" --no-merges -i -E --grep='(^|[^a-z])(fix|bug|revert|hotfix)' --name-only --format= | grep -v '^$' | sort | uniq -c | sort -rn | head -30
```

Churn alone favors small files that are edited often for good reasons (a route table, a changelog). Multiplying by size points at the files that are both large and busy:

```python
"""Files ranked by commits in the window times current line count.
usage: python3 hotspots.py [since] [top]   e.g. python3 hotspots.py "12 months ago" 30"""
import collections, subprocess, sys

since = sys.argv[1] if len(sys.argv) > 1 else "12 months ago"
top = int(sys.argv[2]) if len(sys.argv) > 2 else 30
git = lambda *a: subprocess.run(("git",) + a, capture_output=True, text=True, check=True).stdout
tracked = set(git("ls-files").splitlines())
commits = collections.Counter(
    f for f in git("log", f"--since={since}", "--no-merges", "--name-only", "--format=").splitlines() if f in tracked)
rows = []
for path, n in commits.items():
    try:
        with open(path, encoding="utf-8") as fh:
            lines = sum(1 for _ in fh)
    except (OSError, UnicodeDecodeError):
        continue
    rows.append((n * lines, n, lines, path))
print(f"{'score':>8} {'commits':>7} {'lines':>6}  file")
for score, n, lines, path in sorted(rows, reverse=True)[:top]:
    print(f"{score:>8} {n:>7} {lines:>6}  {path}")
```

First run `git rev-parse --is-shallow-repository`: a shallow clone (common in CI and cloud sandboxes) shows almost no history, so fetch the full history with `git fetch --unshallow` when you may, or treat it as thin. If the repo is younger than a year or has fewer than about 50 commits, the history is too thin to rank by. Say so in the report and rank by dependency edges and marker counts instead.

## What changes together

Pairs of files that land in the same commit. `share` is how often the less-changed file of the pair changes along with the other one.

```python
"""Pairs of files committed together, as a share of the commits of the less-changed file.
usage: python3 cochange.py [since] [min_together] [top]"""
import collections, itertools, subprocess, sys

since = sys.argv[1] if len(sys.argv) > 1 else "12 months ago"
min_together = int(sys.argv[2]) if len(sys.argv) > 2 else 4
top = int(sys.argv[3]) if len(sys.argv) > 3 else 30
git = lambda *a: subprocess.run(("git",) + a, capture_output=True, text=True, check=True).stdout
tracked = set(git("ls-files").splitlines())
log = git("log", f"--since={since}", "--no-merges", "--name-only", "--format=%x01")
total = collections.Counter(); together = collections.Counter()
for commit in log.split("\x01"):
    files = sorted({f for f in commit.splitlines() if f in tracked})
    total.update(files)
    if 2 <= len(files) <= 25:      # a sweeping commit would link everything to everything
        together.update(itertools.combinations(files, 2))
rows = [(n / min(total[a], total[b]), n, a, b) for (a, b), n in together.items() if n >= min_together]
print(f"{'share':>5} {'both':>4}  pair")
for share, n, a, b in sorted(rows, reverse=True)[:top]:
    print(f"{share:>5.0%} {n:>4}  {a}  <->  {b}")
```

Read each pair against the dependency edges:

| Pair | Meaning |
|---|---|
| Co-changes at 60% or more, and one imports the other | Expected: a module and its test, a type and its only user. Not a finding. |
| Co-changes at 60% or more, and no import links them | The code hides a connection. This is the strongest evidence for question 1 in the problem catalog. |
| One imports the other, and they almost never co-change | A healthy boundary. Leave it alone. |

Also measure how wide a typical change is, for the before-and-after numbers:

```sh
git log --since="12 months ago" --no-merges --format=%x01 --name-only | awk 'BEGIN{RS="\001"} NF{print NF}' | sort -n | awk '{a[NR]=$1} END{print "commits", NR, "median files", a[int((NR+1)/2)]}'
```

## Markers worth counting

Count per file first (`-c`); open the files with the highest counts. A single match can be a very long line, so don't print matches across the whole repo.

```sh
git grep -cwE 'TODO|FIXME|HACK|XXX' -- ':!*.md'                                   # known debt
git grep -cE '\.skip\(|(^|[^a-zA-Z])xit\(|xdescribe\(|@pytest\.mark\.skip|t\.Skip\(|#\[ignore\]'  # tests switched off
git grep -cE '(^|[^[:alnum:]_])as any([^[:alnum:]_]|$)|@ts-ignore|@ts-expect-error|# type: ignore|eslint-disable|noqa'   # checks switched off
git grep -cE 'sleep\(|setTimeout\(|time\.Sleep\(|retry'                            # timing and retries
git grep -cE 'catch[[:space:]]*(\([^)]*\))?[[:space:]]*\{[[:space:]]*\}?[[:space:]]*$' -- '*.ts' '*.tsx' '*.js'   # catch blocks to inspect
git grep -cE 'except([[:space:]]+[A-Za-z_.]+)?[[:space:]]*:[[:space:]]*$' -- '*.py'                            # except blocks to inspect
```

In the files with the most catch or except blocks, read them with `git grep -nE -A1 '<pattern>' -- <file>`. A marker is a lead, not a finding. A `setTimeout` that debounces input is the design; one that waits for another module to finish is a workaround.

## Reading the map

Before filling the ledger, write five lines from the map:

1. The areas, and for each one what it is for in a sentence.
2. The direction dependencies should run, and the edges that run against it.
3. The ten files with the highest hotspot score.
4. The co-changing pairs with no import between them.
5. The areas no check covers.

These five lines are also the first section of the report.
