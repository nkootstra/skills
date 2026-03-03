# Analysis Framework Reference

Detailed rubrics and checklists for each of the 13 dimensions. Read when performing an analysis.

---

## Scoring Rubric

Each dimension scored 1-10:

| Score | Meaning |
|-------|---------|
| 9-10 | Exceptional — reduces complexity, teaching-quality |
| 7-8 | Good — principles followed, minor issues |
| 5-6 | Adequate — some followed, some violated |
| 3-4 | Poor — significant problems adding complexity |
| 1-2 | Critical — pervasive violations |

**Letter grade** (from weighted average):

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 8.5+ | Excellent — few improvements needed |
| B | 7.0-8.4 | Good — solid with room for improvement |
| C | 5.5-6.9 | Adequate — significant complexity debt |
| D | 4.0-5.4 | Poor — complexity hinders development |
| F | <4.0 | Critical — major redesign recommended |

**Weighted average formula**:

```
weighted_avg = (
    (dim1 + dim2 + dim3 + dim4) * 1.5 +
    (dim5 + dim6 + dim7 + dim8 + dim9) * 1.2 +
    (dim10 + dim11 + dim12 + dim13) * 1.0
) / (4*1.5 + 5*1.2 + 4*1.0)
```

The grade is a conversation starter, not final judgment. Context matters.

---

## Severity Classification

Every finding gets a severity tag. Use these definitions consistently:

| Severity | Definition | Examples |
|----------|-----------|----------|
| **Critical** | Actively spreading complexity. Blocks safe change. Other code depends on this being wrong. Fix first. | Leaking internal state that 10+ modules depend on; god class accumulating all responsibility; no error handling on critical path |
| **Major** | Significant design issue but contained. Degrades quality but doesn't cascade. | Shallow module with complex interface; temporal decomposition in one subsystem; pass-through layers adding no value |
| **Minor** | Suboptimal but low impact. Fix opportunistically. | Vague variable name; missing interface comment; inconsistent style in one file |

When in doubt, ask: "If this stays unfixed for 6 months, does it get worse on its own?" Critical = yes (complexity spreads). Major = stays the same. Minor = nobody notices.

---

## Dimensions

### 1. Module Depth (Core — weight 1.5x)

**Principle**: Best modules provide powerful functionality behind simple interfaces. Deep = small interface, rich implementation. Shallow = complex interface, little functionality.

**Good signs**: Few public methods doing a lot internally; simple signatures hiding complex logic; common case needs minimal args; good defaults.

**Bad signs**: Many tiny methods doing little; one-liner wrappers; "classitis"; public API nearly as large as implementation; callers must understand internals.

**Measure**: Pick 5-10 key classes. Calculate depth ratio: `implementation_lines / public_method_count`. Low (<5-10) = shallow. High (>30-50) = deep. Check if public methods genuinely hide complexity.

**Scoring**: 9-10: Most modules deep, simple APIs, good defaults | 7-8: Generally deep, few shallow utilities ok | 5-6: Mix of deep/shallow, some classitis | 3-4: Predominantly shallow, trivial methods | 1-2: Pervasive shallowness, getter/setter bags

---

### 2. Information Hiding (Core — weight 1.5x)

**Principle**: Each module encapsulates design decisions. Implementation knowledge should not appear in interfaces or leak to other modules.

**Good signs**: Implementation details invisible to callers; internals can change without affecting API; private members >> public; modules own their domain knowledge; format/protocol details in one place.

**Bad signs**: Same format knowledge in multiple classes (e.g., separate reader/writer both knowing file format); getters exposing internal data structures; returning raw collections; config spread across modules; two classes always modified together.

**Measure**: Search for shared knowledge between modules. Check mutual imports. Look for exposed internal data structures. Find duplicated constants/magic numbers across files.

**Scoring**: 9-10: Cleanly encapsulated, changes localized | 7-8: Mostly hidden, minor leakage | 5-6: Some hiding, noticeable leakage | 3-4: Significant leakage, multi-module changes | 1-2: No encapsulation, tight coupling

---

### 3. Abstraction Quality (Core — weight 1.5x)

**Principle**: An abstraction is a simplified view omitting unimportant details. Good abstractions include exactly the right details — no more (complexity), no less (obscurity).

**Good signs**: Interfaces understood without reading implementation; match problem domain; functions do one thing completely; clean what/how separation; designed for common case.

**Bad signs**: False abstractions (appear simple, require internal knowledge); leaky abstractions; wrong level (too high/low); temporal decomposition (organized by when, not what); half-done tasks requiring callers to finish.

**Measure**: Can you describe each major module in 1-2 sentences? Do callers need to know "how", or just "what"? Any false abstractions?

**Scoring**: 9-10: Crisp, right level, self-contained | 7-8: Mostly clean, few at wrong level | 5-6: Some leaky or wrong-level | 3-4: Many false/missing, callers must know internals | 1-2: No meaningful abstractions

---

### 4. Complexity Indicators (Core — weight 1.5x)

**Principle**: Complexity = change amplification (small changes → many edits) + cognitive load (lots to learn) + unknown unknowns (can't know what you need to know).

**Change Amplification**: Duplicated constants/values; synchronized changes across files; no single source of truth.

**Cognitive Load**: Many parameters (>4-5); deep nesting (>3-4 levels); complex conditionals; global/shared mutable state; implicit ordering (must call A before B); non-obvious side effects.

**Unknown Unknowns**: Dependencies invisible in imports; action at a distance; no cross-module contract docs; implicit undocumented conventions.

**Measure**: Trace a hypothetical change ("rename a field", "add a type") — how many files touched? Count parameters on key functions. Find deeply nested code. Search for global/singleton mutable state.

**Scoring**: 9-10: Localized changes, low cognitive load, few surprises | 7-8: Mostly low, few high-load areas | 5-6: Moderate, some amplification/hidden deps | 3-4: High, changes ripple, hidden gotchas | 1-2: Extreme, small changes feel dangerous

---

### 5. Error Handling (Structural — weight 1.2x)

**Principle**: Exceptions are a major complexity source. Best approach: define errors out of existence, mask at low levels, or aggregate.

**Good signs**: APIs designed so errors can't happen; errors masked at low levels; exception aggregation; sensible defaults eliminating error paths; "just crash" for unrecoverable.

**Bad signs**: Excessive try/catch (one per operation); exceptions for normal situations; catch blocks that re-throw or log-and-ignore; error handling creating more errors; missing handling entirely; overly defensive checks.

**Measure**: Search for exception/error patterns. Ratio of error-handling to business logic. Methods throwing exceptions that could be defined away. Clean propagation vs. cascading complexity.

**Scoring**: 9-10: Elegantly defined away, minimal noise | 7-8: Mostly clean, few unnecessary exceptions | 5-6: Functional but noisy | 3-4: Adds significant complexity, empty catches | 1-2: Broken, missing, or creates more problems

---

### 6. Layering (Structural — weight 1.2x)

**Principle**: Each layer provides a different abstraction. Adjacent layers with the same abstraction = problem.

**Good signs**: Each layer adds meaningful transformation; clear separation (data access, logic, presentation); independently understandable; no pass-through methods; different vocabulary per layer.

**Bad signs**: Pass-through methods adding no value; wrapper classes forwarding calls; many thin layers doing the same thing; mixed concerns; same data structure through all layers unchanged.

**Measure**: Trace a request through layers — does the abstraction change? Count pass-through methods. Check if layers use different vocabulary/types.

**Scoring**: 9-10: Clean distinct layers, no pass-through | 7-8: Good, few pass-throughs | 5-6: Layers often share abstractions | 3-4: Poorly separated, many pass-throughs | 1-2: Everything mixed or everything pass-through

---

### 7. Design Investment (Structural — weight 1.2x)

*Merged from: Strategic vs. Tactical + Design Investment & Evolution*

**Principle**: Strategic programming invests in design for long-term payoff (~10-20% of time). Design is determined more by evolution than initial conception. "If you're not making design better, you're probably making it worse."

**Strategic signs**: "Design it twice" evidence (non-obvious choices suggesting alternatives considered); reusable infrastructure investment; refactoring alongside features in git history; older modules show improvement; tests enable confident refactoring; centralized config; codebase getting better, not just bigger.

**Tactical signs**: TODO/FIXME/HACK everywhere; quick patches over proper fixes; copy-paste code; "tactical tornado" code; no/minimal tests; stale feature flags; god classes accumulating responsibility; "smallest possible change" culture; growing debt never paid; feature branches but no cleanup.

**Measure**:
- Search `TODO`/`FIXME`/`HACK`/`WORKAROUND`/`TEMPORARY`/`XXX` — count them and check dates
- Git history: refactoring vs. feature commit ratio
- Oldest modules improved or just patched?
- Design docs exist (ADRs, design notes)?
- Test coverage/quality

**Scoring**: 9-10: Investment culture, regular refactoring, TODOs resolved, design docs | 7-8: Good habits, debt being addressed | 5-6: Mixed, some investment + shortcuts | 3-4: Mostly tactical, accumulated debt | 1-2: Pure feature factory, maximum debt

---

### 8. Comments & Abstractions (Structural — weight 1.2x)

*Merged from: Comments & Documentation + Comments as Design Tool*

**Principle**: Comments are a design tool, not just documentation. They complete abstractions that code alone cannot express. Without comments, there IS no abstraction. If you can't write a short, clear comment — the design is probably wrong.

**Interface comments (for users)**: Describe "what" and "why", never "how". Use different words than the code. Add precision: units, boundaries, invariants. Enable use without reading implementation.

**Implementation comments (for maintainers)**: Higher-level intuition about what the code does. Cross-module dependency docs. Phase comments in long methods.

**Good**: Interface comments on every public class/method; "write comments first" evidence (class-level design comments, method contracts before bodies); cross-module dependency docs.

**Bad**: No comments; comments repeat code (`// increment i` next to `i++`); same words as code; implementation details in interface docs; stale/contradicting comments.

**Design canary** — what absence reveals:
- No comments → not thinking about abstractions
- Long comments needed → design too complex (Hard to Describe red flag)
- Interface comments describe implementation → shallow module
- Comments get stale → too far from code, or duplicated

**Measure**: Coverage (% of public APIs with interface comments). Quality (sample 10 — do they add info?). Canary test (long/complex comments pointing to design problems?). Freshness.

**Scoring**: 9-10: Complete abstractions, comments-first culture, cross-module docs | 7-8: Good coverage/quality, most interfaces documented | 5-6: Partial, mixed useful/repeating | 3-4: Sparse, missing interfaces, no design docs | 1-2: None or misleading

---

### 9. Codebase Navigability (Structural — weight 1.2x)

**Principle**: Navigable by a zero-context newcomer. A new developer (or AI agent) enters with no memory, just the file tree. Structure should reveal architecture. Interfaces should be readable without implementation. Boundary tests make deep modules trustworthy.

**Good signs**: Folder structure mirrors logical architecture (auth/, billing/); obvious entry points per module; system purpose understood from folder names + interfaces only; public types separated from internals; enforced import boundaries; module-level docs.

**Bad signs**: Flat directories with hundreds of files; no clear entry points; unrestricted imports; unindicative names (utils.ts, helpers.py, misc.go); module groupings only in developers' heads; no module docs.

**Measure**:
- **File tree test**: Can you guess architecture from folder names?
- **Interface discovery**: For 3-5 key modules, find public API without reading implementation?
- **Import graph**: Enforced boundaries?
- **New starter sim**: From file tree, how many files to understand what the system does?

**Scoring**: 9-10: File tree IS architecture diagram, clear boundaries | 7-8: Good structure, most modules discoverable | 5-6: Partial, some clear/some require diving | 3-4: Mostly flat/misleading | 1-2: Must read everything to understand anything

---

### 10. Naming & Obviousness (Surface — weight 1.0x)

**Principle**: Names create precise mental images. Code should be obvious — reader's first guess should be correct.

**Good naming**: Clear image without docs; precise (not `data`/`result`/`manager`); consistent (same name = same concept); boolean predicates (`isReady`, `hasPermission`).

**Poor naming**: Vague (`data`, `value`, `item`, `temp`, `info`, `stuff`); misleading; inconsistent across codebase; obscure abbreviations.

**Measure**: Scan names in key files. Count vague names. Check concept-name consistency. Read methods cold — obvious?

**Scoring**: 9-10: Precise, evocative, reads like prose | 7-8: Mostly good, few vague | 5-6: Mixed | 3-4: Many vague/misleading | 1-2: Names convey nothing

---

### 11. Consistency (Surface — weight 1.0x)

**Principle**: Similar things done similarly. Consistency creates cognitive leverage — learn once, understand everywhere.

**Good**: Uniform style; same patterns for same problems; naming conventions followed; consistent file organization.

**Bad**: Mixed styles (camelCase + snake_case); same problem solved differently; inconsistent file organization; some modules follow conventions, others don't.

**Measure**: Compare similar files — same patterns? Naming conventions project-wide? Error handling consistent? Style guide or linting config present?

**Scoring**: 9-10: Rock-solid, automated enforcement | 7-8: Generally consistent, minor deviations | 5-6: Partly consistent, different conventions per area | 3-4: Multiple competing conventions | 1-2: No consistency

---

### 12. Software Trends Anti-Patterns (Surface — weight 1.0x)

**Principle**: Popular practices can fight or amplify complexity depending on application.

**Getter/Setter Overuse**: Classes mostly getters/setters → information hiding failure. Better: modules perform operations for callers rather than exposing state.

**Implementation Inheritance**: Deep hierarchies (>3 levels) → high coupling. Subclasses needing parent's implementation details. Better: composition over inheritance; interface inheritance.

**Design Pattern Misuse**: Forced patterns (unnecessary Factories, Singletons everywhere). "Pattern-itis" — patterns for their own sake. Only use when they genuinely reduce complexity.

**Agile-Gone-Tactical**: Feature-driven sprints without abstraction time. Increments are features not abstractions.

**TDD-Gone-Tactical**: Tests drive feature-level not abstraction-level thinking. Test-per-method vs. test-per-abstraction.

**Measure**: Getter/setter vs. behavior method ratio. Max inheritance depth. Patterns helping or adding layers? Tests verify abstractions or implementation?

**Scoring**: 9-10: Thoughtful use, patterns fit, shallow inheritance | 7-8: Mostly good, few misapplications | 5-6: Some pattern/inheritance/getter overuse | 3-4: Deep hierarchies, getter bags, forced patterns | 1-2: Cargo-culted practices

---

### 13. Performance-Design Relationship (Surface — weight 1.0x)

**Principle**: Clean design and performance are compatible. Simple code runs faster. Shallow layers cost extra method calls. Special cases on critical paths cost complexity and speed.

**Good balance**: Naturally efficient choices (hash tables over linear scans); clean critical paths; deep modules reducing layer overhead; no premature optimization; allocation-aware design.

**Poor balance**: Death by a thousand cuts (many small inefficiencies); premature optimization adding unmeasured complexity; shallow layers adding call chain overhead; special cases multiplying; no benchmarks.

**Measure**: Method call depth for common operations. Allocation patterns in hot paths. N+1 patterns. Evidence of benchmarks/profiling.

**Scoring**: 9-10: Clean design IS performance strategy | 7-8: Good balance, few unnecessary layers | 5-6: Some perf issues from design, no measurements | 3-4: Design hurts performance | 1-2: Premature optimization everywhere or total ignorance

---

## Ousterhout's Design Principles

Evaluate the project against each:

1. **Complexity is incremental** — small stuff accumulates
2. **Working code isn't enough** — design quality matters equally
3. **Continual small investments** — 10-20% of time on design improvement
4. **Modules should be deep** — simple interfaces, rich functionality
5. **Common case should be simple** — good defaults, minimal config
6. **Simple interface > simple implementation** — callers' ease matters more
7. **General-purpose modules are deeper** — avoid over-specialization
8. **Separate general-purpose and special-purpose** — push specialization up/down
9. **Different layers = different abstractions** — no pass-through layers
10. **Pull complexity downwards** — developers suffer, not users
11. **Define errors out of existence** — simplify error semantics
12. **Design it twice** — consider alternatives before committing
13. **Comments describe non-obvious things** — different level of detail than code
14. **Design for reading, not writing**
15. **Increments = abstractions, not features**
16. **Separate what matters from what doesn't**
17. **Not making design better → making it worse** — continuous evolution

---

## Red Flags

| Red Flag | Signal |
|---|---|
| **Shallow Module** | Interface nearly as complex as implementation |
| **Information Leakage** | Same design decision in multiple modules |
| **Temporal Decomposition** | Structured by execution order, not information hiding |
| **Overexposure** | Common-case users must learn rare features |
| **Pass-Through Method** | Forwards to another method with same signature |
| **Repetition** | Same nontrivial pattern in multiple places |
| **Special-General Mixture** | Special-purpose code in general-purpose mechanisms |
| **Conjoined Methods** | Can't understand one without reading another |
| **Comment Repeats Code** | Restates what code says |
| **Implementation in Interface Docs** | Interface docs describe implementation |
| **Vague Name** | Too generic to convey meaning |
| **Hard to Pick Name** | Naming difficulty → unclear design |
| **Hard to Describe** | Needs long comment → bad abstraction |
| **Nonobvious Code** | Behavior unclear from quick reading |

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
- Interface vs. implementation count — many interfaces with one impl = shallow
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
