"""Per-skill recall/precision, negatives specificity, cost and turns from a `claude plugin eval --json` file.
usage: python3 evals/triggering/summarize.py evals/results/<file>.json"""
import json, sys, math, statistics, collections

SKILLS = ["design-critique","design-exploration","intentional-prototyping","interface-polish","write-readme","write-prose"]
PREFIX = {"crit":"design-critique","expl":"design-exploration","prot":"intentional-prototyping","pol":"interface-polish","readme":"write-readme","prose":"write-prose","none":"none"}
d = json.load(open(sys.argv[1]))
tp = collections.Counter(); pos = collections.Counter(); fp = collections.Counter()
neg_runs = neg_clean = 0; passed = []; costs = []; turns = []; secs = []
rows = []
for c in d["cases"]:
    cid = c["name"].removeprefix("triggering-")
    exp = PREFIX[cid.split("-")[0]]
    for r in c["arms"]["with"]:
        g = {x["name"]: x["passed"] for x in r["graders"]}
        fired_wrong = [n.removeprefix("not-") for n, ok in g.items() if n.startswith("not-") and not ok]
        for s in fired_wrong: fp[s] += 1
        if exp == "none":
            neg_runs += 1; neg_clean += not fired_wrong
        else:
            pos[exp] += 1; tp[exp] += g.get("loads-expected", False)
        passed.append(r["passed"]); costs.append(r["costUsd"]); turns.append(r["turns"]); secs.append(r["durationSeconds"])
        rows.append((cid, exp, r["passed"], fired_wrong, r["turns"], r["costUsd"]))

n = len(passed); p = sum(passed) / n
print(f"pass rate {p:.0%} over {n} runs (±{1.96*math.sqrt(p*(1-p)/n):.0%} 95% CI)")
print(f"{'skill':26} recall      precision")
for s in SKILLS:
    rec = f"{tp[s]}/{pos[s]}" if pos[s] else "-"
    prec_den = tp[s] + fp[s]
    print(f"{s:26} {rec:11} {tp[s]}/{prec_den}" if prec_den else f"{s:26} {rec:11} -")
print(f"negatives specificity      {neg_clean}/{neg_runs}")
print(f"cost/run   median ${statistics.median(costs):.3f}  max ${max(costs):.3f}  total ${sum(costs):.2f}")
print(f"turns/run  median {statistics.median(turns)}  max {max(turns)}   seconds/run median {statistics.median(secs)}  max {max(secs)}")
fails = [r for r in rows if not r[2]]
if fails:
    print("\nfailures:")
    for cid, exp, _, wrong, t, cost in fails:
        print(f"  {cid:10} expected {exp:24} fired instead: {', '.join(wrong) or 'nothing'}")
