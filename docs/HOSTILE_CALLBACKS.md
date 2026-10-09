# Hostile callback support

Test-only paper, no repository authority or execution acceptance. Complete source/tests/docs must be measured; reject oversize without trimming coverage.

## API and limitations
`CallbackCounts = dict[str, int]`; `CALLBACK_NAMES` is exactly `("len", "iter", "str", "repr", "eq", "bool", "getitem", "get")`.
Supply a native mutable dictionary with all eight counters initially zero; `HostileString(value, counts)` additionally needs a native string.
`HostileObject(counts)`, `HostileDict(counts)`, and `HostileList(counts)` retain caller counters by identity; constructors invoke no hostile operations; containers start empty.
Typed `HostileString.__new__` creates actual native backing. Base descriptors intentionally bypass hostile overrides for safe backing inspection.
All four fixtures override len/iter/str/repr/eq/bool/getitem; dict additionally overrides get. Each operation increments only its own counter once, then raises `RuntimeError(name)`.
Counters are intentional caller-owned effects, not validated against hostile/malformed input. No implicit shared state.
`Never` annotates always-raising operations compatibly with Python3.11 base return types; normal-return mutation targets use ordinary return annotations.
Equality follows subclass semantics, including ordinary hash disabling: no hashability promise. Fixtures are not production-safe, snapshots, concurrency primitives, or security boundaries; never production defaults.

## Coverage inventory H01–H05
- H01 `test_constructor_safety_and_isolation`: exact types/native backing through base descriptors, zero constructor callbacks, retained counter identity, independent caller dictionaries and untouched sibling state.
- H02 `test_operation_matrix`: explicit applicability table covers all29 class/operation pairs. Safe static labels, reset counters per row, native control has no counter effect; first/second independent invocation checks exact exception args and all eight counts. Iteration uses `iter`, not a constructor invoking length.
- H03 `test_target_tcin_consumer`: real shipped predicate (never replaced), native leading-zero positive/invalid negatives, each hostile root exactFalse, zero callbacks, identity/backing retained.
- H04 `test_bounded_json_tree_consumer`: real shipped guard (never replaced), selected native tcin/title positive, all hostile roots and independent hostile metadata descendants exactFalse, independent native metadata counterparts exactTrue. Identity/selected fields/backing unchanged; all counters zero including dict.get and descendant callbacks; assertions outside production catch.
- H05 `test_silence_and_caller_ownership`: capture stdout/stderr around direct probes and consumer calls; direct exceptions caught in tests, explicit reset/caller edits/retained ownership and independent state. No extraction/private/live/product proof.

## H06 external-only causal mutations
Use separate disposable complete module copies, no committed runner/mutants. Each exact old block below must match once; abort otherwise, preserve all other source.
All named kills are `HostileCallbackTests.test_operation_matrix`; constructor-isolation also kills missing len increment.

1. Missing increment: replace `def __len__(self) -> int:\n    self._hit("len")` with `def __len__(self) -> int:\n    raise RuntimeError("len")`; len assertions expect1 but observe0.
2. Wrong name: replace `def __iter__(self) -> Never:\n    self._hit("iter")` with `def __iter__(self) -> Never:\n    self.counts["len"] += 1\n    raise RuntimeError("iter")`; complete count comparison catches wrong entries despite correct exception.
3. Normal return: replace `def __str__(self) -> str:\n    self._hit("str")` with `def __str__(self) -> str:\n    return "normal"`; str rows detect missing RuntimeError, valid str return.

Here `\n` denotes a newline; blocks are shown relative to method indentation. Add the existing four-space class indentation to every line for exact matching.
Every mutant must import, compile and type-check; syntax/import/type errors are NOT assertion kills. Record substitutions/matchcounts/baseline+mutant commands/exits/named assertions/original+final hashes. Original/restored baseline passes, source hashes unchanged.

## H07 full admission and execution gates
Public dependency base `66355e86e88ae236f34ae821f2e961b3e763015f`:
- `agent_household/target_tcin.py` SHA256 `0b32c714d589095fb6fe5a9b93b6bf8670634223003cc75a41e4f253d39ca988`.
- `agent_household/json_tree.py` SHA256 `edde6f94f60f09f66ac61e7b9a15ee4c66daba345dc93028e17cb9fae6c61b02`.
Dependency bodies were supplied to tools-disabled author; parent must verify exact bytes/pins and reject drift. Establish exclusive ownership and exact freshbase before implementation.
Run `/Users/mfethe/.local/bin/python3.11 -B -m unittest discover -s tests -v`: retain43 existing+five new tests, no skips.
Across ALL `agent_household` and `tests`: isolated no-cache Ruff targetpy311 select `E,F,W,I,UP,B,A,C4,SIM,RUF,ANN`, plus full isolated formattercheck.
External Basedpyright config strict Python3.11, include both full directories, worktree+tests extraPaths, exact interpreter `/Users/mfethe/.local/bin/python3.11`; no exclusions/suppressions/Any/settings weakening.
External-cache compileall, gitdiff whitespace checks, exact three-file scope, all formatted additions+deletions<=399 including docs; AST fragments are not complete allocations.
Implementation issue, independent executed review/mutation receipts, parent publication and fresh merged verification required; paper/size alone not admission. Rollback only owned isolated changes.

## Deferred obligations
Support does not discharge recordR01–R09/staticwiring/six consumer mutants, wholepage #33 F01–F12, #29 D01–D04, Costco/Amazon or other retailers, live inventory/price/pickup/labels, private household/shared expenses, historical REAL_CALL_PROBE status cleanup.
Recount full record only after support actually ships; no budget guarantee or product acceptance.

## Explicit preservation and downstream obligations
Preserve both the453-line rejected original and345-line rejected revision as read-only evidence; reject oversized candidates without deleting them or inferring source-reuse authority. Correctedpaper has no repository authority until admission.
Deferred record requirements retain ownership/input identity, silence, exact raw-string semantics, valid guard-control pairs, real trace consumers, ordinary-exception catch, cancellation propagation, recovery/priorhook restoration, static dependency wiring and all six record mutations.
Live stock as well as inventory/price/pickup/labels remains unaccepted. No partial extractor commit: retain all original consumer assertions, recount complete consumer only after support ships, and never claim support as record/module/page or product acceptance.
