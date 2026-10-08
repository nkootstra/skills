"""Writes cases.jsonl and cases.md for the triggering eval. Edit CASES, rerun."""
import json, pathlib

# (id, expected, also_ok, difficulty, prompt)
# expected: the skill that should load, or "none". also_ok: other skills that are acceptable to load too.
CASES = [
# design-critique
("crit-01","design-critique",[],"direct","Can you critique the settings page in src/pages/Settings.tsx? Be specific."),
("crit-02","design-critique",[],"indirect","Something about our onboarding screen just feels off and I can't put my finger on it. What's wrong with it? It's in src/pages/Onboarding.tsx."),
("crit-03","design-critique",[],"indirect","Here are two versions of the pricing card (PricingA.tsx and PricingB.tsx in src/components). Which one is better and why?"),
("crit-04","design-critique",[],"indirect","Before I show this dashboard to my manager tomorrow, tell me honestly what's weak about it. src/pages/Dashboard.tsx"),
("crit-05","design-critique",[],"indirect","We keep saying our app should feel 'calm and trustworthy'. Can you score the current UI against that and tell me where it falls short?"),
("crit-06","design-critique",["interface-polish"],"hard","Is the checkout flow in src/pages/Checkout.tsx good enough to ship, visually? Just give me your assessment, don't change anything."),
("crit-07","design-critique",[],"hard","Do a heuristic evaluation of the signup form in src/components/SignupForm.tsx."),
("crit-08","design-critique",[],"hard","My designer friend said the header 'has no hierarchy'. Is she right? What does that even mean here? src/components/Header.tsx"),
# design-exploration
("expl-01","design-exploration",[],"direct","Give me a few genuinely different design directions for an empty state on the projects page."),
("expl-02","design-exploration",[],"indirect","I need to design how users split a bill with friends in our app. What are some ways this could work? Don't build anything yet."),
("expl-03","design-exploration",[],"indirect","Our file upload is a boring dropzone. How could it be way better? I want options, not code."),
("expl-04","design-exploration",[],"indirect","I keep landing on the same layout for the landing page hero and it looks like every other SaaS site. Help me get out of that rut."),
("expl-05","design-exploration",["design-critique"],"hard","Here's my first idea for the notification center (src/components/Notifications.tsx). Before I commit, what else could it be?"),
("expl-06","design-exploration",[],"hard","What would onboarding look like if it had no screens at all?"),
("expl-07","design-exploration",["interface-polish"],"hard","The search component works but it's a 3 out of 10. Walk me through taking it to a 9, step by step, as ideas first."),
("expl-08","design-exploration",[],"hard","Brainstorm 10 concepts for a habit tracker's daily check-in. Make the later ones weird."),
# intentional-prototyping
("prot-01","intentional-prototyping",[],"direct","Prototype a card that flips over when you tap it, I want to see if it feels good."),
("prot-02","intentional-prototyping",[],"indirect","I want to dial in the spring on our drawer opening. Can you make something where I can tweak stiffness and damping live?"),
("prot-03","intentional-prototyping",[],"indirect","Saw this effect on a site where the button kind of melts into a toast when you click it. How would I rebuild that?"),
("prot-04","intentional-prototyping",[],"indirect","Make a quick throwaway page to test whether a swipe-to-archive gesture on list rows makes sense. Just gray boxes is fine."),
("prot-05","intentional-prototyping",[],"indirect","I can't decide on the shadow for the floating panel. Build me something with sliders for blur, offset and opacity so I can try values."),
("prot-06","intentional-prototyping",[],"hard","How did Linear do that command menu open animation? I want to recreate it to understand it."),
("prot-07","intentional-prototyping",["design-exploration"],"hard","Show me 12 random variations of this tooltip's entrance animation in a grid so I can pick one."),
("prot-08","intentional-prototyping",[],"hard","Before we build the real thing, I want to know if a radial menu is even understandable. What's the fastest way to find out?"),
# interface-polish
("pol-01","interface-polish",[],"direct","Polish the settings page so it feels premium. src/pages/Settings.tsx"),
("pol-02","interface-polish",[],"indirect","We're launching Monday. Go through src/pages/Dashboard.tsx and make it feel finished: empty states, loading, errors, all of it."),
("pol-03","interface-polish",[],"indirect","The app works but looks like a hackathon project. Make the team members list in src/components/TeamList.tsx not look generic."),
("pol-04","interface-polish",[],"indirect","Add proper loading, empty and error states to the invoices table in src/components/InvoiceTable.tsx."),
("pol-05","interface-polish",["design-critique"],"hard","This is going in my portfolio. Make the project card component as good as it can possibly be. src/components/ProjectCard.tsx"),
("pol-06","interface-polish",[],"hard","Build a settings page for notification preferences. It should feel native and high quality, not like a default template."),
("pol-07","interface-polish",[],"hard","Make the modal in src/components/Modal.tsx feel right: how it opens, closes, focus, escape, all the details."),
("pol-08","interface-polish",[],"hard","Clean up the dark mode on the marketing page, the cards look washed out and the screenshots glow. src/pages/Home.tsx"),
# none: adjacent tasks the skills should stay out of
("none-01","none",[],"near-miss","Fix the TypeError in src/components/InvoiceTable.tsx: 'Cannot read properties of undefined (reading map)'."),
("none-02","none",[],"near-miss","Convert #4F46E5 to HSL and OKLCH."),
("none-03","none",[],"near-miss","Write a commit message for the changes I just made to the header."),
("none-04","none",[],"near-miss","Explain the difference between flexbox and CSS grid."),
("none-05","none",[],"near-miss","Rename the Button component's 'kind' prop to 'variant' everywhere."),
("none-06","none",[],"near-miss","Add a unit test for the formatCurrency util in src/utils/format.ts."),
("none-07","none",[],"near-miss","Change the primary button color to #0F766E."),
("none-08","none",[],"near-miss","Set up Tailwind in this project."),
("none-09","none",[],"near-miss","What's the CSS property for making text not wrap?"),
("none-10","none",[],"near-miss","Write the API route that returns the list of invoices as JSON."),
("none-11","none",[],"near-miss","Update the copyright year in the footer to 2026."),
("none-12","none",[],"near-miss","Why is my Next.js build failing with 'Module not found: Can't resolve @/lib/db'?"),
]

here = pathlib.Path(__file__).parent
with open(here/"cases.jsonl","w") as f:
    for cid, exp, ok, diff, prompt in CASES:
        f.write(json.dumps({"id":cid,"expected":exp,"also_ok":ok,"tags":[exp,diff],"prompt":prompt})+"\n")

lines=["# Triggering eval cases","",f"{len(CASES)} cases. `expected` is the skill that should load (or `none`); `also ok` lists other skills that may load without counting as a false positive.","","| id | expected | also ok | difficulty | prompt |","|---|---|---|---|---|"]
for cid, exp, ok, diff, prompt in CASES:
    lines.append(f"| {cid} | {exp} | {', '.join(ok) or ''} | {diff} | {prompt.replace('|','/')} |")
(here/"cases.md").write_text("\n".join(lines)+"\n")
print(len(CASES))

# ---- case directories for `claude plugin eval` ----
PILOT = {"crit-02","crit-06","expl-02","prot-03","pol-02","pol-05","none-01","none-07"}
SKILLS = ["design-critique","design-exploration","intentional-prototyping","interface-polish"]
def rx(names):
    alt = "|".join(names)
    return r'"skill"\s*:\s*"(?:[\w-]+:)?(?:' + alt + r')"'

def grader(path, fields, body=""):
    fm = "\n".join(f"{k}: {v}" for k, v in fields.items())
    path.write_text(f"---\n{fm}\n---\n{body}")

for cid, exp, ok, diff, prompt in CASES:
    d = here / cid
    (d / "graders").mkdir(parents=True, exist_ok=True)
    for old in (d / "graders").glob("*.md"):
        old.unlink()
    (d / "prompt.md").write_text(
        "---\n"
        f"name: triggering-{cid}\n"
        f"tags: [triggering, {exp}, {diff}{', pilot' if cid in PILOT else ''}]\n"
        "runs: 2\n"
        "plugins: [\"../../..\"]\n"
        "max_turns: 4\n"
        "timeout_seconds: 240\n"
        "allowed_tools: [Read, Glob, Grep, Skill]\n"
        f"expected_outcome: {'Loads ' + exp if exp != 'none' else 'Loads none of the design skills'}\n"
        "---\n"
        f"{prompt}\n")
    others = SKILLS if exp == "none" else [s for s in SKILLS if s != exp and s not in ok]
    if exp != "none":
        grader(d / "graders" / "loads-expected.md",
               {"type": "tool_used", "tool": "Skill", "input_match": f"'{rx([exp])}'", "min": 1, "weight": len(others) or 1})
    for s in others:
        grader(d / "graders" / f"not-{s}.md",
               {"type": "tool_used", "tool": "Skill", "input_match": f"'{rx([s])}'", "min": 0, "max": 0})
print("case dirs written")
