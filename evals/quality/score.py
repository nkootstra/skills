"""Scores improve-codebase runs: did behavior stay the same, and did the structure get better.
`claude plugin eval` has no grader that runs a command, so this runs after the eval, on workspaces kept with --keep-temp.

usage: python3 evals/quality/score.py score <fixture> <label>=<dir> [<label>=<dir> ...]
       python3 evals/quality/score.py record <fixture>        record the untouched fixture's outputs as its golden
       python3 evals/quality/score.py verify [<fixture> ...]  fail unless each fixture replays its history, passes its
                                                             tests and still produces its golden outputs (CI runs this)

<dir> is a kept sandbox directory (the eval prints "kept /private/tmp/e-..."; open it first with the chmod it prints)
or any folder holding the repo. The repo is copied out before anything runs: never run git inside a kept directory.

The "checks" object in fixtures/<name>.json:
  run          command prefix for the public interface, e.g. ["python3", "-m", "parcel"]
  calls        argument lists whose output must not change
  trap         argument lists that exercise a planted bug; unchanged output means the bug was left for the user to decide
  tests        the fixture's test command
  marker       a path that identifies the repo root inside a kept directory
  source       {"include": regex, "exclude": regex} on relative paths: the files the counts look at
  counts       name -> regex; occurrences across source files, lower is better
  file_counts  name -> regex; number of source files with a match, lower is better
  tests_regex  {"include": regex, "pattern": regex}: counts test functions
  cycles       "python" or "js": count modules that sit in an import cycle
  facts        what a judge needs to know about the fixture (used by make_cases.py)"""
import ast, os, pathlib, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fixture_repo

IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "node_modules", ".build_repo.py")

def run(cmd, cwd):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
        return {"code": p.returncode, "out": p.stdout}
    except Exception as exc:
        return {"code": -1, "out": type(exc).__name__}

def source_files(repo, spec):
    out = {}
    for p in sorted(repo.rglob("*")):
        rel = p.relative_to(repo).as_posix()
        if p.is_file() and re.search(spec["include"], rel) and not (spec.get("exclude") and re.search(spec["exclude"], rel)):
            try:
                out[rel] = p.read_text()
            except UnicodeDecodeError:
                pass
    return out

def python_edges(src):
    names = {}
    for rel in src:
        parts = rel[:-3].split("/")
        names[".".join(parts[:-1] if parts[-1] == "__init__" else parts)] = rel
    graph = {n: set() for n in names}
    for n, rel in names.items():
        try:
            tree = ast.parse(src[rel])
        except SyntaxError:
            continue
        pkg = n.split(".") if rel.endswith("__init__.py") else n.split(".")[:-1]
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Import):
                targets = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = (pkg[:len(pkg) - node.level + 1] if node.level else []) + (node.module.split(".") if node.module else [])
                targets = [".".join(base)] + [".".join(base + [a.name]) for a in node.names]
            graph[n].update(t for t in targets if t in names and t != n)
    return graph

def js_edges(src):
    graph = {rel: set() for rel in src}
    pattern = re.compile(r"""(?:\bfrom|\bimport|\brequire\()\s*['"](\.{1,2}/[^'"]+)['"]""")
    for rel, text in src.items():
        for target in pattern.findall(text):
            base = os.path.normpath(os.path.join(os.path.dirname(rel), target)).replace(os.sep, "/")
            for candidate in (base, base + ".js", base + ".mjs", base + "/index.js"):
                if candidate in src and candidate != rel:
                    graph[rel].add(candidate)
                    break
    return graph

def in_cycles(graph):
    def reaches(a, b, seen):
        for nxt in graph[a]:
            if nxt == b:
                return True
            if nxt not in seen:
                seen.add(nxt)
                if reaches(nxt, b, seen):
                    return True
        return False
    return sorted(n for n in graph if reaches(n, n, set()))

def measure(repo, spec, golden, original):
    row = {}
    if golden:
        same = sum(run(spec["run"] + a, repo) == want for a, want in golden["calls"])
        trap = sum(run(spec["run"] + a, repo) == want for a, want in golden["trap"])
        row["behavior unchanged"] = f"{same}/{len(golden['calls'])}"
        row["planted bug left as is"] = f"{trap}/{len(golden['trap'])}"
        row["_changed"] = [" ".join(a) for a, want in golden["calls"] if run(spec["run"] + a, repo) != want][:6]
    row["tests pass"] = "yes" if run(spec["tests"], repo)["code"] == 0 else "NO"
    everything = source_files(repo, {"include": "."})
    if "tests_regex" in spec:
        t = spec["tests_regex"]
        row["test functions"] = sum(len(re.findall(t["pattern"], body)) for rel, body in everything.items() if re.search(t["include"], rel))
    src = source_files(repo, spec["source"])
    for name, pattern in spec.get("file_counts", {}).items():
        row[name] = sum(1 for body in src.values() if re.search(pattern, body))
    for name, pattern in spec.get("counts", {}).items():
        row[name] = sum(len(re.findall(pattern, body)) for body in src.values())
    if spec.get("cycles"):
        row["modules in import cycles"] = len(in_cycles(python_edges(src) if spec["cycles"] == "python" else js_edges(src)))
    row["source files"] = len(src)
    row["source lines"] = sum(len(body.splitlines()) for body in src.values())
    row["files changed"] = sum(1 for rel in set(everything) | set(original) if everything.get(rel) != original.get(rel))
    return row

def find_repo(path, marker):
    path = pathlib.Path(path)
    hits = sorted((p for p in path.rglob(pathlib.PurePosixPath(marker).name) if p.as_posix().endswith(marker)), key=lambda p: len(p.parts))
    if not hits:
        raise SystemExit(f"no {marker} under {path} (a kept directory has to be opened with chmod first)")
    return pathlib.Path(str(hits[0])[: -len(marker)].rstrip("/"))

def verify(names):
    failed = False
    for name in names:
        fixture_repo.states(name)   # raises if the history no longer replays
        spec, golden = fixture_repo.checks(name), fixture_repo.load(name)["golden"]
        with tempfile.TemporaryDirectory() as tmp:
            fixture_repo.write_files(name, tmp)
            problems = []
            if run(spec["tests"], tmp)["code"] != 0:
                problems.append("its tests fail")
            for kind in ("calls", "trap"):
                if [a for a, _ in golden[kind]] != spec[kind]:
                    problems.append(f"golden {kind} were recorded for a different list; run: score.py record {name}")
                bad = [" ".join(a) for a, want in golden[kind] if run(spec["run"] + a, tmp) != want]
                if bad:
                    problems.append(f"{len(bad)} {kind} differ from golden, e.g. {bad[0]}")
        print(f"{'✗' if problems else '✓'} {name}: " + ("; ".join(problems) if problems else
              f"history replays, tests pass, {len(golden['calls'])} + {len(golden['trap'])} outputs match"))
        failed |= bool(problems)
    sys.exit(1 if failed else 0)

def main():
    mode = sys.argv[1]
    if mode == "verify":
        return verify(sys.argv[2:] or fixture_repo.names())
    name = sys.argv[2]
    spec = fixture_repo.checks(name)
    original = fixture_repo.files(name)
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "baseline"
        fixture_repo.write_files(name, base)
        if mode == "record":
            data = fixture_repo.load(name)
            data["golden"] = {"calls": [[a, run(spec["run"] + a, base)] for a in spec["calls"]],
                              "trap": [[a, run(spec["run"] + a, base)] for a in spec["trap"]]}
            fixture_repo.save(name, data)
            codes = sorted({r["code"] for _, r in data["golden"]["calls"] + data["golden"]["trap"]})
            print(f"{name}: {len(spec['calls'])} calls and {len(spec['trap'])} trap calls recorded, exit codes {codes}")
            return
        golden = fixture_repo.load(name)["golden"]
        rows = {"baseline": measure(base, spec, golden, original)}
        for arg in sys.argv[3:]:
            label, _, given = arg.partition("=")
            copy = pathlib.Path(tmp) / label
            shutil.copytree(find_repo(given, spec["marker"]), copy, ignore=IGNORE)
            rows[label] = measure(copy, spec, golden, original)
    keys = [k for k in rows["baseline"] if not k.startswith("_")]
    print("| measure | " + " | ".join(rows) + " |")
    print("|---|" + "---|" * len(rows))
    for k in keys:
        print(f"| {k} | " + " | ".join(str(r.get(k, "-")) for r in rows.values()) + " |")
    for label, r in rows.items():
        if r.get("_changed"):
            print(f"\n{label}: output changed for: " + "; ".join(r["_changed"]))

if __name__ == "__main__":
    main()
