# Problem catalog

Five questions, and for each the shapes a bad answer takes. Every shape has a **confirm** step: the evidence that turns a suspicion into a ledger entry. If the confirm step comes back empty, drop the suspicion.

The **usual fix** is a starting point. The real fix is chosen in step 5 of the workflow, once entries are grouped under a cause, and it is often one change for several shapes at once.

## Contents

- [1. Where does a change land?](#1-where-does-a-change-land)
- [2. What does this lean on?](#2-what-does-this-lean-on)
- [3. Can the reader trust it?](#3-can-the-reader-trust-it)
- [4. Does each piece earn its place?](#4-does-each-piece-earn-its-place)
- [5. Will a break be noticed?](#5-will-a-break-be-noticed)
- [Workarounds](#workarounds)
- [What is not a finding](#what-is-not-a-finding)

## 1. Where does a change land?

Good answer: adding a field, a variant or a rule means editing one place, and the compiler or a test points to any other.

| Shape | Confirm | Usual fix |
|---|---|---|
| The same rule written in several places (a validation, a price calculation, a permission check) | Grep for the rule's literal values or its key expression; the co-change list shows the copies moving together | One definition that the others call. Copies that differ in a value are the same rule with a parameter. Text that looks alike but takes different steps encodes different rules and is not this shape: leave it. |
| A list that must be kept in step with another list by hand (enum and its labels, routes and nav items, events and their handlers) | Find a past commit that updated one and a later fix that updated the other | Derive one from the other, or make one table both read from |
| One feature spread over folders named for technical layers | Pick three recent feature commits and count the folders each touched; three or more is the signal | Move the feature's files next to each other; keep a shared layer only for code several features use |
| A variant added by editing a `switch` or `if` chain in many files | Grep for the discriminating value; count the sites | Put what varies behind one interface or one lookup table per variant |
| Knowledge of a data shape repeated at every use (parsing, defaults, null checks) | Count the sites that touch the raw shape | Parse once at the boundary into a type the rest can rely on |

## 2. What does this lean on?

Good answer: each module names its inputs, depends on things that change less often than it does, and can be read without opening its dependencies' internals.

| Shape | Confirm | Usual fix |
|---|---|---|
| A hidden input: a global, a singleton, an environment read, the clock, or a file another module writes | Grep for the read; check whether a test has to set it up out of band | Pass it in as a parameter or constructor argument |
| A required call order nothing enforces (`init()` before `load()`, `open` before `use`) | Find a caller that gets it wrong, or a comment warning about it | Make the first call return the thing the second call needs, so the wrong order doesn't compile |
| Callers reaching into a module's internals (deep imports, private fields, knowledge of its storage) | List imports that skip the module's entry point | Widen the entry point by what callers really need, then close the internals |
| Core logic importing a volatile detail (domain code that imports the HTTP client, the ORM model, a vendor SDK) | Compare churn: the dependency changes more often than the code depending on it | Have the core define the small interface it needs; the detail implements it |
| An import cycle between areas | The edge listing in mapping.md marks them | Move the shared piece to a third place both depend on, or invert the weaker edge |
| A general function that knows about one caller (a `mode` or `isAdminExport` parameter) | The parameter is passed by exactly one call site | Split the caller-specific part back out to that caller |

## 3. Can the reader trust it?

Good answer: a name says what the thing does, a type says what it can be, and the same job is done the same way everywhere.

| Shape | Confirm | Usual fix |
|---|---|---|
| A name that no longer matches (`getUser` that also writes, `utils` holding domain rules, `temp`, `new`, `v2`) | Read the body against the name | Rename to what it does. If no honest name is short, the thing is doing two jobs: split it. |
| Two ways to do one job (two HTTP wrappers, two date libraries, two state patterns) | Count the uses of each | Pick the one with more uses or the better fit, migrate the other, delete it. A half-finished migration is the most common source. |
| A type wider than the values it holds (`string` for a status, optional fields that are always set, `any`) | Collect the actual values from call sites and data | Narrow the type so impossible states don't typecheck |
| A comment that contradicts the code, or describes a previous version | Read the two side by side; `git log -L` on the lines shows when they diverged | Fix or delete the comment (rules in safe-changes.md) |
| A function long enough that its steps can't be seen at once, with steps at mixed levels of detail | Over about 60 lines and a reader has to scroll to learn what it returns | Extract the steps that have a name; don't extract a step only to shorten the function |
| A boolean parameter or a positional argument list that reads as noise at the call site (`render(true, false, null)`) | Read three call sites without opening the definition | Named options, or two functions |

## 4. Does each piece earn its place?

Good answer: every file, layer, option and abstraction exists because something today needs it.

| Shape | Confirm | Usual fix |
|---|---|---|
| Code nothing reaches (unused exports, unreachable branches, feature flags fixed at one value, files no entry point imports) | Grep for references across the repo, including dynamic lookups, config, templates and scripts; check the flag's value in every environment config | Delete it. Git keeps the history. |
| A layer that forwards without adding anything (a service that only calls the repository with the same arguments) | Every method is a one-line pass-through | Remove the layer and call through, unless it is the seam a test or a second implementation uses today |
| An interface with one implementation and no test double | Count implementations | Use the concrete type until a second one exists |
| Options, hooks or config keys nobody sets to anything but the default | Grep call sites and config files for the option | Remove the option and the branch behind it |
| An abstraction that needs an escape hatch at most call sites | Count the call sites that pass the override or reach around it | The abstraction is cut along the wrong line: inline it, then extract along what the call sites share |
| A module so thin its interface is as big as its body | Compare the signature count with the logic | Merge it into its one caller, or deepen it so it hides a decision |

## 5. Will a break be noticed?

Good answer: changing behavior fails a check, and changing structure without changing behavior fails none.

| Shape | Confirm | Usual fix |
|---|---|---|
| A test that cannot fail | Break the code it covers (flip a condition, return a constant) and run it; it still passes | Rewrite it to assert an outcome, or delete it |
| A test tied to internals (asserts on private calls, mock call order, a snapshot of markup nobody reviews) | A refactor with no behavior change turns it red | Rewrite it against the public entry point and observable result |
| A test that swaps the repo's own modules for stand-ins, so those modules never run together | Break one of the replaced modules, or change the unit or shape of what it returns; the suite stays green because no test runs the real ones side by side | Run the real modules together and keep stand-ins only for what lies outside the repo (the network, the clock, a payment provider). If the real run shows wrong behavior, assert what the code does today and add an ASK. |
| A test that restates the implementation (computes the expected value with the same formula) | The expected value is derived, not written down | Replace the derivation with literal examples |
| An error swallowed or turned into a default (`catch {}`, `except: pass`, `?? []` on a failed fetch) | Read each match from the marker scan; decide whether the caller can tell success from failure | Let it propagate to the layer that can act on it, or return a result the caller must handle |
| An unchecked boundary (JSON parsed straight into a trusted type, an untyped cast on external data) | Find where data enters and whether anything validates it | Validate at entry |
| Checks switched off (`skip`, `ts-ignore`, lint disables) | The marker scan; `git blame` for how long | Fix the cause and re-enable, or delete the test if the behavior is gone |
| Checks too slow to run after every step | The baseline timings from step 2 | Report it. Speeding up the suite is its own piece of work: mark it ASK unless it is a one-line configuration fix. |

## Workarounds

A workaround gets one situation through by stepping around the normal path. It is rarely wrong where it stands, which is why it survives review. Record each one with the situation it serves:

| Kind | Looks like |
|---|---|
| Identity checks | A branch on one named customer, route, tenant or caller; an argument only one call site ever passes |
| Reaching across | A flag one module sets so that another skips part of its job; state reset by hand before calling something |
| Buying time | A delay or timer whose purpose is ordering; a re-read or retry around an operation that has no reason to fail |
| Silencing | A caught error nobody handles; a disabled test, assertion or lint rule |
| Warnings | A `// don't touch`, `// order matters` or `// keep in sync with` comment |

Then sort the workarounds by situation, across files. Three or more for one situation mean the normal path doesn't cover a case the product needs. Name what is missing (a lifecycle, an ownership rule, a shared registry, a state the type doesn't model) and make that the REDESIGN entry. A workaround with no siblings may be a real exception: LEAVE it, with a comment stating the outside fact it depends on.

## What is not a finding

- Code that is old, written in an unfashionable style, or not how you would have written it.
- A long file that is long because the thing it describes is long (a schema, a route table, a fixture).
- Similar-looking code that encodes different rules and changes independently.
- An inconsistency in an area with no commits in the window and no dependents that change.
- Missing tests, by themselves. Record the area as report-only and move on, unless a planned change needs the behavior pinned.
- Generated or vendored code (lockfiles, `vendor/`, generated clients, files marked generated). A problem there is fixed in its source or generator, or not at all.
- Formatting, import order and anything a formatter or linter fixes. That belongs to the project's tooling, not to this pass.
