# Range Techniques

How to generate directions that are structurally different, how to tell range from variants, and how to present and choose between them.

## Start from the job

Before generating, write the job to be done in one line: "When <situation>, I want to <motivation>, so I can <outcome>." Range is generated against the job, not the screen. "Help people split a bill" invites calculators; "When the check arrives, I want to settle up without awkwardness, so the evening ends well" invites directions that remove the moment entirely. Directions that serve the job but have no screen are often the strongest.

## What "structurally different" means

Two directions are structurally different when they differ on at least one **mechanism axis**. Visual style, layout, color and copy are not mechanism axes: changing only those produces variants.

| Axis | Question | Example values |
| --- | --- | --- |
| **Input model** | How does intent get in? | Direct manipulation, form fields, presets, natural language, camera, gesture, inference from existing data |
| **Who acts** | How much does the person do vs. the system? | Fully manual, assisted (system suggests), supervised (system does, person confirms), automatic (no step at all) |
| **Metaphor / domain** | What is it "like"? | Ledger, conversation, game, physical object, ritual, marketplace, map, timeline |
| **Time model** | When does it happen? | Instant (in the moment), scheduled (later, batched), ambient (continuous, in the background), retrospective (after the fact) |
| **Density** | How much is shown at once? | One decision per screen, a dashboard of everything, progressive disclosure, a single number |
| **Surface** | Where does it live? | Screen, notification, voice, email, physical object, someone else's app, none |
| **Social shape** | Who else is involved? | Solo, one-to-one, group, public, delegated to a third party |

The first six are the core set. Social shape matters whenever more than one person touches the outcome.

## Range or variant? The test

For any pair of directions, ask:

1. **Can you describe the core mechanism of each in one sentence without mentioning visuals?** If both sentences are the same, it's a variant.
2. **Which axis differs?** Name it. If you can't name an axis from the table, it's a variant.
3. **Would a different person prefer each, for a reason?** Range produces directions where the trade-off is real and someone would choose the "worse" one. Variants usually have an obvious winner.
4. **Would building one teach you something the other can't?** If prototyping A answers B's question too, they're the same direction.

Two "no"s on questions 2 to 4 means merge them.

## Prompt bank

Use these when the first three ideas have come out and the well feels dry. Answer each prompt literally, even when it seems absurd, then adapt back.

### Remove or add a constraint

- What if there were no screen at all? What would the person have to do, and what would the system have to know?
- What if it had to be done in three seconds, one-handed, while walking?
- What if it happened automatically and the person only found out afterwards?
- What if the person could not type anything, only choose or point?
- What if it had to work for someone doing it for the first time and someone doing it for the hundredth time, with the same interface?
- What if it cost the person nothing, not even a tap, unless something went wrong?

### Borrow from a domain

- How would a game designer make this: what is the score, the turn, the win state?
- How would this work as a physical object on a table: what do you touch, what does it weigh?
- What ritual already exists around this (a toast, a handshake, a receipt) and could the design be that ritual?
- How would a brand with a strong point of view do it: a bank, a luxury hotel, a children's toy, a utility company?
- How does a profession that does this all day handle it: a waiter, an accountant, an air traffic controller?
- What would the version from 1985 look like, and what did it get right?

**Borrowing a visual movement.** When range is about look and feel rather than mechanism, borrow a documented movement instead of reaching for adjectives like "modern" or "clean", which pull toward the average. Each comes with rules you can actually apply:

| Movement | Rules to apply |
| --- | --- |
| **Swiss / International Typographic Style** | Strict grid, asymmetric layout, one sans-serif family, hierarchy from size and position, no ornament. |
| **Bauhaus** | Geometric primitives, primary colors plus black, form follows function, type set on axes. |
| **Neo-brutalism** | Visible structure: thick borders, hard offset shadows, flat saturated fills, default-looking type used on purpose. |
| **Editorial / magazine** | Expressive display type, varied column widths, large imagery, pull quotes, generous margins. |
| **Dieter Rams** | As little design as possible: neutral palette, one accent for the one thing that matters, nothing decorative. |
| **Platform-native** (Apple HIG, Material) | Inherit the whole system: navigation, type scale, motion, components. The safest baseline, the hardest to make distinctive. |

Name one movement per direction and state its rules in the direction's description. Two movements blended in one direction usually produce neither.

### Avoid the generic AI aesthetic

This is the default every direction drifts toward unless named: purple-to-blue gradients, everything centered, a hero with a vague headline and two buttons, three feature cards with emoji or line icons, glassmorphism panels, one sans-serif (usually Inter) at every level, uniform rounded corners and soft shadows on everything. If a direction could be described this way, it isn't a direction yet. Treat it like a variant: change the core decision (type, layout model, color strategy) before presenting it.

None of these is banned. The failure is landing on one because nobody chose. For each direction, state its primary color, typeface, layout model and radius strategy in one line each; any that you can't justify is a default, not a decision.

### Invert the problem

- Instead of helping people choose, help them eliminate.
- Instead of the person telling the system, the system tells the person and they correct it.
- Instead of preventing the mistake, make the mistake cheap to undo.
- Instead of doing it now, make it someone else's job later.
- Instead of making it faster, make it unnecessary.
- Instead of one person doing it for many, everyone does a small part.

### Set a quota

- Write 12 directions. Stop only when you have 12, even if 9 to 12 feel silly.
- After every 4, check the mechanism axes: which column has nobody touched yet? Write the next one there.
- Write one direction per surface value (screen, notification, voice, physical, none).
- Write one direction per "who acts" value, from fully manual to fully automatic.
- Write the direction you would be embarrassed to show, then find the part of it that isn't embarrassing.

### Max out one quality

- What is the 10/10 version on speed, where nothing else matters?
- On fairness or accuracy?
- On delight: what would someone screenshot and send to a friend?
- On calm: what is the version that never interrupts?
- On distinctiveness: what would be unmistakably this product's and no one else's?
- On trust: what would a skeptical person need to see to believe it?

## Worked example: "Help people split a restaurant bill"

### Wrong: three variants

1. **Itemized list, card style.** Scan the receipt, each item is a card, tap to assign to a person.
2. **Itemized list, table style.** Same, but as a compact table with checkboxes per person.
3. **Itemized list, colorful.** Same, each person gets a color, items fill with their color when tapped.

All three share one mechanism: scan, then manually assign items to people. They differ only in density and styling. This is depth on one concept, presented as if it were range.

### Right: eight directions

| Name | Core mechanism | Main trade-off | Best when |
| --- | --- | --- | --- |
| **Claim it** | Receipt is shared to the table's phones; each person taps the items they had, and leftovers are split evenly | Accurate and self-serve, but needs everyone to have the app and pay attention | Groups of friends with uneven orders |
| **Even split, with exceptions** | Default is equal shares; anyone can flag "I only had a salad" and the rest rebalance | Fast for the common case, but the person with the exception has to speak up | Groups who roughly ate the same |
| **One payer, settle later** | One person pays; the app records who owes what and nudges the debts over the following days | No friction at the table, but debts linger and someone carries the cost | Recurring groups who trust each other |
| **Running tab** | No per-meal split at all; balances accumulate across many meals and settle when they cross a threshold | Nearly zero effort per meal, but less clarity about any single meal | Housemates, colleagues who eat together weekly |
| **Bill roulette** | Spin to pick who pays this time, weighted by who has paid least recently | Fun and memorable, but only fair over many meals | Close friends who enjoy the game |
| **Order-time split** | Each person's order is tagged to them at the moment of ordering, through the restaurant's system; the bill arrives already split | No splitting step exists, but it depends on restaurant integration | Restaurants with table ordering |
| **Voice at the table** | Someone says "Sam had the steak and two beers, the rest is even" and the split is computed | Hands-free and social, but error-prone and awkward in loud rooms | Small groups, simple orders |
| **Pot first** | Everyone puts a fixed amount into a shared pot before the meal; the pot pays and refunds the remainder | Removes the end-of-meal moment entirely, but needs planning ahead | Group dinners, trips, events |

Axes covered: input model (tap, voice, none), who acts (each person, one person, system), time model (instant, later, accumulated, before), metaphor (ledger, game, pot), surface (phone, restaurant system, voice). No two share a mechanism.

Note how "Running tab" and "One payer, settle later" were close: both defer payment. They stay separate because they differ on time model (per meal vs. accumulated) and would be chosen by different groups. If they had differed only in how reminders look, they'd be merged.

## The merge rule

If two directions share a core mechanism, merge them into one direction and keep the better execution detail from each as a note. Do not pad a list with near-duplicates to hit a quota: the quota exists to push past the obvious, not to inflate the count. After merging, if the list is short, go back to the mechanism axes and fill an empty column.

## Presenting range

Use this table, one row per direction:

```markdown
| Name | Core mechanism | Main trade-off | Best when |
| --- | --- | --- | --- |
| **Short name** | One sentence, no visuals, says what happens | The one thing you give up | The situation or person it suits |
```

Rules:

- **Name**: two or three words, evocative enough to refer back to in conversation ("let's go with Pot first").
- **Core mechanism**: describes behavior, not appearance. "Cards with avatars" is not a mechanism.
- **Main trade-off**: one honest cost per direction. If a direction has no cost, you haven't thought about it long enough.
- **Best when**: a context, not a judgment. This is where the facet fit shows.
- Order the table from most conventional to most unusual, so the reader's assumptions get stretched gradually.
- Keep it to 5 to 8 rows when presenting, even if you generated 12 or 20. Cut the weakest, keep the widest spread.

## Choosing and recommending

Always end range with a recommendation. A table without a pick pushes the hard part back onto the user.

Weigh each direction on three things:

1. **Facet fit.** Which direction scores highest on the product's quality facets (speed, trust, delight, whatever this product is about)? If a design-critique pass is available, score each direction against the facets explicitly.
2. **Risk.** What has to be true for this direction to work (an integration, a behavior change, a technology), and how likely is it? A direction with high fit and one unproven dependency is often the right pick, as long as that dependency gets tested first.
3. **Learning value.** Which direction, if prototyped, would answer the most questions about the others? Sometimes the best first build is not the likely winner but the one that resolves the biggest uncertainty.

Format the recommendation as:

```markdown
**Recommendation: <Name>.** <Why it wins on facet fit, in one or two sentences.>
The main risk is <risk>; test it first by <cheapest way to find out>.
Worth keeping in mind: <runner-up>, if <condition under which the runner-up would win>.
```

Hybrids are allowed but suspicious. "Even split with exceptions, plus Running tab for regulars" can be a strong product, but propose it only after picking a primary mechanism. A hybrid proposed first usually means no choice was made.

## Checklist before presenting

- [ ] At least four mechanism axes are represented across the set.
- [ ] At least one direction removes the interface or the step entirely.
- [ ] No direction is the generic AI aesthetic in disguise.
- [ ] No two directions pass the merge test.
- [ ] Every row has an honest trade-off.
- [ ] The first idea you had is in the list, labeled honestly, not hidden or inflated.
- [ ] There is a recommendation with a risk and a way to test it.
