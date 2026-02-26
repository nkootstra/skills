# Analysis Framework Reference

Detailed rubrics and checklists for each dimension. Read when performing an analysis.

## Scoring Rubric

Each dimension scored 1-10:

| Score | Meaning |
|-------|---------|
| 9-10 | Exceptional — reduces complexity, teaching-quality |
| 7-8 | Good — principles followed, minor issues |
| 5-6 | Adequate — some followed, some violated |
| 3-4 | Poor — significant problems adding complexity |
| 1-2 | Critical — pervasive violations |

**Overall grade** (weighted average → letter):

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 8.5+ | Excellent — few improvements needed |
| B | 7.0-8.4 | Good — solid w/ room for improvement |
| C | 5.5-6.9 | Adequate — significant complexity debt |
| D | 4.0-5.4 | Poor — complexity hinders development |
| F | <4.0 | Critical — major redesign recommended |

---

## 1. Module Depth

**Principle**: Best modules provide powerful functionality behind simple interfaces. Deep = small interface, rich implementation. Shallow = complex interface, little functionality.

**Good signs**: Few public methods doing a lot internally; simple signatures hiding complex logic; common case needs minimal args; good defaults
**Bad signs**: Many tiny methods doing little; one-liner wrappers; "classitis"; public API nearly as large as implementation; callers must understand internals

**Measure**: Pick 5-10 key classes. Calculate depth ratio: `implementation_lines / public_method_count`. Low (<5-10) → shallow. High (>30-50) → deep. Check if public methods genuinely hide complexity.

**Scoring**: 9-10: Most modules deep, simple APIs, good defaults | 7-8: Generally deep, few shallow utilities ok | 5-6: Mix of deep/shallow, some classitis | 3-4: Predominantly shallow, trivial methods | 1-2: Pervasive shallowness, getter/setter bags

---

## 2. Information Hiding

**Principle**: Each module encapsulates design decisions. Implementation knowledge should not appear in interfaces or leak to other modules.

**Good signs**: Implementation details invisible to callers; internals can change w/o affecting API; private members >> public; modules own their domain knowledge; format/protocol details in one place
**Bad signs**: Same format knowledge in multiple classes (e.g., separate reader/writer both knowing file format); getters exposing internal data structures; returning raw collections; config spread across modules; two classes always modified together

**Measure**: Search for shared knowledge between modules. Check mutual imports. Look for exposed internal data structures. Find duplicated constants/magic numbers across files.

**Scoring**: 9-10: Cleanly encapsulated, changes localized | 7-8: Mostly hidden, minor leakage | 5-6: Some hiding, noticeable leakage | 3-4: Significant leakage, multi-module changes | 1-2: No encapsulation, tight coupling

---

## 3. Abstraction Quality

**Principle**: An abstraction is a simplified view omitting unimportant details. Good abstractions include exactly the right details — no more (complexity), no less (obscurity).

**Good signs**: Interfaces understood w/o reading implementation; match problem domain; functions do one thing completely; clean what/how separation; designed for common case
**Bad signs**: False abstractions (appear simple, require internal knowledge); leaky abstractions; wrong level (too high/low); temporal decomposition (organized by when, not what); half-done tasks requiring callers to finish

**Measure**: Can you describe each major module in 1-2 sentences? Do callers need to know "how", or just "what"? Any false abstractions?

**Scoring**: 9-10: Crisp, right level, self-contained | 7-8: Mostly clean, few at wrong level | 5-6: Some leaky or wrong-level | 3-4: Many false/missing, callers must know internals | 1-2: No meaningful abstractions

---

## 4. Complexity Indicators

**Principle**: Complexity = change amplification (small changes → many edits) + cognitive load (lots to learn) + unknown unknowns (can't know what you need to know).

**Change Amplification**: Duplicated constants/values; synchronized changes across files; no single source of truth
**Cognitive Load**: Many parameters (>4-5); deep nesting (>3-4 levels); complex conditionals; global/shared mutable state; implicit ordering (must call A before B); non-obvious side effects
**Unknown Unknowns**: Dependencies invisible in imports; action at a distance; no cross-module contract docs; implicit undocumented conventions

**Measure**: Trace a hypothetical change ("rename a field", "add a type") — how many files touched? Count parameters on key functions. Find deeply nested code. Search for global/singleton mutable state.

**Scoring**: 9-10: Localized changes, low cognitive load, few surprises | 7-8: Mostly low, few high-load areas | 5-6: Moderate, some amplification/hidden deps | 3-4: High, changes ripple, hidden gotchas | 1-2: Extreme, small changes feel dangerous

---

## 5. Error Handling

**Principle**: Exceptions are a major complexity source. Best approach: define errors out of existence, mask at low levels, or aggregate.

**Good signs**: APIs designed so errors can't happen; errors masked at low levels; exception aggregation; sensible defaults eliminating error paths; "just crash" for unrecoverable
**Bad signs**: Excessive try/catch (one per operation); exceptions for normal situations; catch blocks that re-throw or log-and-ignore; error handling creating more errors; missing handling entirely; overly defensive checks

**Measure**: Search for exception/error patterns. Ratio of error-handling to business logic. Methods throwing exceptions that could be defined away. Clean propagation vs. cascading complexity.

**Scoring**: 9-10: Elegantly defined away, minimal noise | 7-8: Mostly clean, few unnecessary exceptions | 5-6: Functional but noisy | 3-4: Adds significant complexity, empty catches | 1-2: Broken, missing, or creates more problems

---

## 6. Naming & Obviousness

**Principle**: Names create precise mental images. Code should be obvious — reader's first guess should be correct.

**Good naming**: Clear image w/o docs; precise (not `data`/`result`/`manager`); consistent (same name = same concept); distinguishes similar things; boolean predicates (`isReady`, `hasPermission`)
**Poor naming**: Vague (`data`, `value`, `item`, `temp`, `info`, `stuff`); misleading; inconsistent across codebase; too similar for different things; obscure abbreviations; Hungarian notation
**Obviousness**: Behavior immediately clear; good whitespace; simple control flow; meaningful types (named struct vs. `Pair<Integer, Boolean>`)

**Measure**: Scan names in key files. Count vague names (`data`, `result`, `handler`, `utils`, `helper`). Check concept-name consistency. Read methods cold — obvious?

**Scoring**: 9-10: Precise, evocative, reads like prose | 7-8: Mostly good, few vague | 5-6: Mixed good/poor | 3-4: Many vague/misleading | 1-2: Names convey nothing

---

## 7. Comments & Documentation

**Principle**: Comments describe things not obvious from code. Interface comments = "what" (for users). Implementation comments = "why" (for maintainers).

**Good**: Interface comments on every public class/method; describe "what"/"why" not "how"; use different words than code; add precision (units, boundaries, invariants); higher-level intuition; cross-module dependency docs
**Poor**: No comments; repeat code (`// increment i` next to `i++`); same words as code; implementation details in interface docs; stale/contradicting; describe "how"

**Measure**: Check public interfaces for comments. Sample 5-10 — do they add info? Look for code-restating comments. Check if complex methods have "what is this doing" comments.

**Scoring**: 9-10: All public APIs documented, comments add real value | 7-8: Good coverage, mostly useful | 5-6: Partial, mixed quality | 3-4: Sparse/low-quality, missing interfaces | 1-2: None or misleading

---

## 8. Consistency

**Principle**: Similar things done similarly. Consistency creates cognitive leverage — learn once, understand everywhere.

**Good**: Uniform style; same patterns for same problems; naming conventions followed; consistent file organization; design patterns applied consistently
**Bad**: Mixed styles (camelCase + snake_case); same problem solved differently; inconsistent file organization; some modules follow conventions, others don't

**Measure**: Compare similar files — same patterns? Check naming conventions project-wide. Error handling consistent? Style guide or linting config present?

**Scoring**: 9-10: Rock-solid, automated enforcement | 7-8: Generally consistent, minor deviations | 5-6: Partly consistent, different conventions per area | 3-4: Multiple competing conventions | 1-2: No consistency

---

## 9. Layering

**Principle**: Each layer provides a different abstraction. Adjacent layers w/ same abstraction → problem.

**Good**: Each layer adds meaningful transformation; clear separation (data access, logic, presentation); independently understandable; no pass-through methods; different vocabulary per layer
**Bad**: Pass-through methods adding no value; wrapper classes forwarding calls; many thin layers doing the same thing; mixed concerns; same data structure through all layers unchanged

**Measure**: Trace a request through layers — abstraction changes? Count pass-through methods. Check if layers use different vocabulary/types. Evaluate wrapper classes.

**Scoring**: 9-10: Clean distinct layers, no pass-through | 7-8: Good, few pass-throughs | 5-6: Layers often share abstractions | 3-4: Poorly separated, many pass-throughs | 1-2: Everything mixed or everything pass-through

---

## 10. Strategic vs. Tactical

**Principle**: Strategic = invest in design for long-term payoff. Tactical = shortcuts for short-term speed at complexity cost.

**Strategic signs**: "Design it twice" evidence; reusable infrastructure investment; comments-first approach; refactoring alongside features; test infrastructure enabling change; centralized config; "write for readers" mentality
**Tactical signs**: TODO/FIXME/HACK everywhere; quick patches over proper fixes; copy-paste code; "tactical tornado" code; no/minimal tests; stale feature flags; god classes accumulating responsibility

**Measure**: Search for TODO/FIXME/HACK/WORKAROUND/TEMPORARY. Check git history for refactoring commits. Test coverage/quality. Evidence of "design it twice". Count duplicated blocks.

**Scoring**: 9-10: Clearly strategic, clean design, good tests | 7-8: Mostly strategic, some tactical corners | 5-6: Mixed, some investment + quick fixes | 3-4: Mostly tactical, accumulated debt | 1-2: Purely tactical, maximum debt

---

## 11. Design Investment & Evolution

**Principle**: Good design requires ~10-20% ongoing investment. Design is determined more by evolution than initial conception. "If you're not making design better, you're probably making it worse." (Ch.3, 16)

**Investment signs**: "Design it Twice" thinking (non-obvious choices suggesting alternatives considered); refactoring alongside features in git history; older modules show improvement; tests enable confident refactoring; centralized config; codebase getting better, not just bigger
**Neglect signs**: "Smallest possible change" culture; growing TODO/HACK count w/o resolution; accumulating special-case if-branches; stale comments contradicting code; no refactoring commits; feature branches but no cleanup; acknowledged debt never paid

**Measure**: Search `TODO`/`FIXME`/`HACK`/`WORKAROUND`/`TEMPORARY`/`XXX` — count and check dates. Git: refactoring vs. feature commit ratio. Oldest modules improved or just patched? Design docs exist (designNotes, ADRs)?

**Scoring**: 9-10: Investment culture, regular refactoring, TODOs resolved, design docs | 7-8: Good habits, debt being addressed | 5-6: Mixed, some investment + shortcuts | 3-4: Mostly neglected, patches on patches | 1-2: Pure feature factory

---

## 12. Software Trends Anti-Patterns

**Principle**: Popular practices can fight or amplify complexity depending on application. (Ch.19)

**Getter/Setter Overuse**: Classes mostly getters/setters → information hiding failure. Better: modules perform operations for callers rather than exposing state.

**Implementation Inheritance**: Deep hierarchies (>3 levels) → high coupling. Subclasses needing parent's implementation details. Instance variables shared between parent/child. Better: composition over inheritance; interface inheritance.

**Design Pattern Misuse**: Forced patterns (unnecessary Factories, Singletons everywhere). "Pattern-itis" — patterns for their own sake. Better: only when they genuinely reduce complexity.

**Agile-Gone-Tactical**: Feature-driven sprints w/o abstraction time. Increments are features not abstractions. Debt sprints that never happen. Better: each increment = an abstraction.

**TDD-Gone-Tactical**: Tests drive feature-level not abstraction-level thinking. Test-per-method vs. test-per-abstraction. Better: TDD for bug fixes; design abstractions before coding.

**Measure**: Getter/setter vs. behavior method ratio. Max inheritance depth. Patterns helping or adding layers? Abstraction-level design work in issues? Tests verify abstractions or implementation?

**Scoring**: 9-10: Thoughtful use, patterns fit, shallow inheritance | 7-8: Mostly good, few misapplications | 5-6: Some pattern/inheritance/getter overuse | 3-4: Deep hierarchies, getter bags, forced patterns | 1-2: Cargo-culted practices

---

## 13. Performance-Design Relationship

**Principle**: Clean design and performance are compatible. Simple code runs faster (avoids extraneous work). Shallow layers cost extra method calls. Special cases on critical paths cost complexity and speed. (Ch.20)

**Good balance**: Naturally efficient choices (hash tables over linear scans); clean critical paths w/ few special cases; deep modules reducing layer overhead; no premature optimization; allocation-aware design
**Poor balance**: Death by a thousand cuts (many small inefficiencies); premature optimization adding unmeasured complexity; shallow layers adding call chain overhead; special cases multiplying on critical paths; no benchmarks; OR total performance ignorance

**Check**: Hot loops w/ unnecessary allocations? Critical paths through many shallow layers? N+1 query patterns? Simpler data structures that would be faster? Naturally efficient alternatives?

**Measure**: Method call depth for common operations. Allocation patterns in hot paths. N+1 patterns. Evidence of benchmarks/profiling. Special-case checks on critical paths.

**Scoring**: 9-10: Clean design IS performance strategy | 7-8: Good balance, few unnecessary layers | 5-6: Some perf issues from design, no measurements | 3-4: Design hurts performance | 1-2: Premature optimization everywhere or total ignorance

---

## 14. Comments as Design Tool

**Principle**: Comments are a design tool, not just documentation. Can't write a short clear comment → design is probably wrong. Comments complete abstractions code alone cannot express. W/o comments, there IS no abstraction. (Ch.12, 13, 15)

**Abstraction completers (good)**: Interface comments enabling use w/o reading code; different detail level than code; describe "what"/"why" never "how"; variable comments specifying units/boundaries/invariants; higher-level conceptual framework; cross-module dependency docs

**Design canary (what absence reveals)**:
- No comments → not thinking about abstractions
- Repeat method names → not thinking beyond code
- Long comments needed → design too complex (Hard to Describe red flag)
- Interface comments describe implementation → shallow module
- Comments get stale → too far from code, or duplicated

**"Write Comments First" test**: Comments placed as design artifacts (before code)? Or bolted on after? Comments-first: class-level design comments, method contracts before bodies, phase comments in long methods. Comments-last: sparse, mirror code structure, clustered at file tops.

**Maintenance signals**: Comments near code they describe? Docs duplicated (→ guaranteed staleness)? Commit message comments that should be in code? designNotes file for cross-module decisions?

**Measure**: Coverage (% of public APIs w/ interface comments), quality (sample 10 — add info?), canary test (long/complex comments?), freshness, detail level, placement, cross-module docs.

**Scoring**: 9-10: Complete abstractions, comments-first culture, cross-module docs | 7-8: Good coverage/quality, most interfaces documented | 5-6: Partial, mixed useful/repeating | 3-4: Sparse, missing interfaces, no design docs | 1-2: None or misleading

---

## 15. Codebase Navigability

**Principle**: Navigable by zero-context newcomer. AI agent or new developer enters like "the guy from Memento" — no memory, just the file tree. File system progressively discloses complexity: structure reveals architecture, interfaces readable w/o implementation, boundary tests make deep modules trustworthy.

**Good signs**: Folder structure mirrors logical architecture (auth/, billing/); obvious entry points per module (index, public API, types); system purpose understood from folder names + interfaces only; public types separated from internals; enforced import boundaries (barrel exports, package.json exports, Go packages, Rust mod.rs, Python `__all__`); deep modules tested at interface boundary (graybox); module-level docs

**Bad signs**: Flat directories w/ hundreds of files; no clear entry points; unrestricted imports; unindicative names (utils.ts, helpers.py, misc.go); module groupings only in developers' heads; tests coupled to implementation; no module docs

**Measure**:
- **File tree test**: `tree`/`ls` at root — can you guess architecture from folder names?
- **Interface discovery**: For 3-5 key modules, find public API w/o reading implementation?
- **Import graph**: Enforced boundaries? (barrel exports, package boundaries, lint rules)
- **Graybox test**: Tests exercise public interface or internal methods/state?
- **New starter sim**: From file tree, how many files to understand what system does?

**Scoring**: 9-10: File tree IS architecture diagram, clear boundaries, graybox tests | 7-8: Good structure, most modules discoverable | 5-6: Partial, some clear/some require diving | 3-4: Mostly flat/misleading, web of imports | 1-2: Must read everything to understand anything

---

## Language-Specific Guidance

### JavaScript/TypeScript
- `any` type abuse (information hiding killer)
- Barrel exports (index.ts) — false module boundaries?
- Callback hell vs. clean async/await
- React components — deep (encapsulate state) or shallow (wrappers)?
- Prop drilling (pass-through variable pattern)

### Python
- `__init__.py` defining public interfaces properly?
- Class sizes — thin wrapper culture?
- Exception handling — bare `except:` is a red flag
- Type hints — improving or noise?
- `__all__` defined (interface clarity)?

### Java/Kotlin
- Classitis (especially common in Java)
- Class hierarchy depth — over-engineering?
- Interface vs. implementation count — many interfaces w/ one impl = shallow
- Builder pattern — value or boilerplate?
- Dependency injection — modularity or complexity?

### Go
- Interface sizes — small per idiom, but should be deep
- `if err != nil` repetition patterns
- Packages as meaningful abstractions vs. file organization
- Godoc comments on exported functions

### Rust
- Trait design — deep abstractions or type wrangling?
- `?` chains — clean or noisy?
- `pub` visibility — used judiciously?
- Lifetime annotation complexity — simplifiable?

---

## Grading Scale

**High weight** (core structural design):
- Module Depth (1), Information Hiding (2), Abstraction Quality (3), Complexity Indicators (4)

**Medium weight** (structural/process):
- Error Handling (5), Layering (9), Strategic vs. Tactical (10), Design Investment (11), Comments as Design Tool (14), Navigability (15)

**Standard weight** (surface-level/situational):
- Naming (6), Comments & Docs (7), Consistency (8), Trends Anti-Patterns (12), Performance-Design (13)

```
weighted_avg = (
    (dim1 + dim2 + dim3 + dim4) * 1.5 +
    (dim5 + dim9 + dim10 + dim11 + dim14 + dim15) * 1.2 +
    (dim6 + dim7 + dim8 + dim12 + dim13) * 1.0
) / (4*1.5 + 6*1.2 + 5*1.0)
```

Map weighted average to letter grade above.

The grade is a conversation starter, not final judgment. Context matters — a weekend prototype at "D" is fine; a production system at "D" needs attention.
