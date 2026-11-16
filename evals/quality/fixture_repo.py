"""Fixture repos for the improve-codebase quality cases.

A fixture lives in fixtures/<name>/:
  files/         the repo as the agent finds it
  history.json   commits, oldest first: {"date", "message", "edits": [[path, before, after]]}; before null = the commit adds the file
  checks.json    how score.py measures a run (see score.py)
  golden.json    recorded output of the untouched fixture, written by `score.py record`

The history is stored as text replacements on the final files, so files/ stays the single copy of the code.
scaffold(name) returns a shell script that rebuilds the repo with that history in an empty workspace."""
import json, pathlib

here = pathlib.Path(__file__).parent

def root(name):
    return here / "fixtures" / name

def files(name):
    base = root(name) / "files"
    return {str(p.relative_to(base)): p.read_text() for p in sorted(base.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}

def checks(name):
    return json.loads((root(name) / "checks.json").read_text())

def states(name):
    """[(date, message, files)] oldest first, ending at files/."""
    history = json.loads((root(name) / "history.json").read_text())
    current = files(name)
    final = dict(current)
    out = []
    for commit in reversed(history["commits"]):
        out.append((commit["date"], commit["message"], dict(current)))
        for path, before, after in reversed(commit["edits"]):
            if before is None:
                del current[path]
                continue
            if current[path].count(after) != 1:
                raise SystemExit(f"{name}: '{commit['message']}' expects one match in {path}, found "
                                 f"{current[path].count(after)}: {after[:60]!r}")
            current[path] = current[path].replace(after, before)
    out.append((history["initial"]["date"], history["initial"]["message"], dict(current)))
    out.reverse()
    assert out[-1][2] == final
    return out, history["author"]

BUILD = '''import json, os, pathlib, subprocess
COMMITS = json.loads(%r)
NAME, EMAIL = %r, %r

def git(*args, date=None):
    env = dict(os.environ)
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", "-c", "user.name=" + NAME, "-c", "user.email=" + EMAIL, "-c", "commit.gpgsign=false",
                    "-c", "init.defaultBranch=main", *args], check=True, env=env, stdout=subprocess.DEVNULL)

git("init")
for date, message, changed in COMMITS:
    for path, body in changed.items():
        if body is None:
            os.remove(path)
            continue
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(path).write_text(body)
    git("add", "-A")
    git("commit", "-m", message, date=date)
'''

def scaffold(name):
    seq, author = states(name)
    commits, previous = [], {}
    for date, message, current in seq:
        changed = {p: b for p, b in current.items() if previous.get(p) != b}
        changed.update({p: None for p in previous if p not in current})
        commits.append([date, message, changed])
        previous = current
    build = BUILD % (json.dumps(commits), author["name"], author["email"])
    # fed on stdin, so the build script never lands in the workspace or its history
    return "set -e\npython3 - <<'BUILD_EOF'\n" + build + "BUILD_EOF\n"

if __name__ == "__main__":
    import sys
    seq, _ = states(sys.argv[1])
    for date, message, current in seq:
        print(date[:10], f"{len(current):>3} files ", message)
