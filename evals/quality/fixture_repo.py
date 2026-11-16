"""Fixture repos for the improve-codebase quality cases, one JSON file each in fixtures/<name>.json:

  files     path -> contents: the repo as the agent finds it
  history   {"author", "initial": {date, message}, "commits": [{date, message, edits: [[path, before, after]]}]}
            commits oldest first, stored as text replacements on the final files; before null = the commit adds the file
  checks    how score.py measures a run (see score.py)
  golden    recorded output of the untouched fixture, written by `score.py record`

To edit a fixture's code, unpack it, change the files, pack it back, then record its outputs again:
  python3 evals/quality/fixture_repo.py unpack parcel /tmp/parcel
  python3 evals/quality/fixture_repo.py pack parcel /tmp/parcel
  python3 evals/quality/score.py record parcel
`python3 evals/quality/fixture_repo.py history parcel` lists the commits and fails if the history no longer replays."""
import json, pathlib, sys

here = pathlib.Path(__file__).parent

def path(name):
    return here / "fixtures" / f"{name}.json"

def load(name):
    return json.loads(path(name).read_text())

def save(name, data):
    path(name).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")

def names():
    return sorted(p.stem for p in (here / "fixtures").glob("*.json"))

def files(name):
    return dict(load(name)["files"])

def checks(name):
    return load(name)["checks"]

def write_files(name, out):
    out = pathlib.Path(out)
    for rel, body in files(name).items():
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)

def states(name):
    """[(date, message, files)] oldest first, ending at the fixture's files."""
    data = load(name)
    history, current = data["history"], dict(data["files"])
    final = dict(current)
    out = []
    for commit in reversed(history["commits"]):
        out.append((commit["date"], commit["message"], dict(current)))
        for rel, before, after in reversed(commit["edits"]):
            if before is None:
                del current[rel]
                continue
            if current[rel].count(after) != 1:
                raise SystemExit(f"{name}: '{commit['message']}' expects one match in {rel}, found "
                                 f"{current[rel].count(after)}: {after[:60]!r}")
            current[rel] = current[rel].replace(after, before)
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
    """Shell script that rebuilds the fixture, history included, in an empty workspace."""
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

def main():
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == "unpack":
        write_files(name, sys.argv[3])
        print(f"{name}: {len(files(name))} files written to {sys.argv[3]}")
    elif cmd == "pack":
        src = pathlib.Path(sys.argv[3])
        data = load(name)
        data["files"] = {p.relative_to(src).as_posix(): p.read_text() for p in sorted(src.rglob("*"))
                         if p.is_file() and not {"__pycache__", "node_modules", ".git"} & set(p.relative_to(src).parts)}
        save(name, data)
        states(name)
        print(f"{name}: {len(data['files'])} files packed; history still replays. Now run: python3 evals/quality/score.py record {name}")
    elif cmd == "history":
        seq, _ = states(name)
        for date, message, current in seq:
            print(date[:10], f"{len(current):>3} files ", message)
    else:
        raise SystemExit(__doc__)

if __name__ == "__main__":
    main()
