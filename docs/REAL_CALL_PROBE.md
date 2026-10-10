# Real-call probe: independent PAPER prerequisite

## Status and scope

These three complete file bodies are an external paper proposal only.
No repository writes, execution, admission, product acceptance, or measured
formatted-size acceptance is claimed. Formatting and all receipts remain pending.
No rejected record source is reused. No production files or package markers change.

`tests/real_call_probe.py` exposes typed `probe_calls(operation, target, events,
failure=None)`. It invokes the operation once, returns its exact result, appends
`call` for each Python call whose code object is identical to `target`, and can
raise `failure()` at that entry. Exceptions propagate without wrapping. Assertions
are exclusively in consumer tests, never in the trace callback.

The previous trace is restored in `finally`, including cancellation and failures
from installation where restoration is possible. It is NOT chained while the
probe is active. This is process-local, current-thread, synchronous support:
no other-thread interception, concurrency guarantee, or native-call completeness.
Existing `sys.settrace` restrictions and failures propagate; restoration itself
is subject to those same restrictions. No credentials or runtime settings change
apart from the temporary trace. No target wrapping, copying, patching, or mocking.

## Consumer coverage

`tests/test_real_call_probe.py` imports `real_call_probe` directly. Discovery with
`unittest discover -s tests -v` supplies that import path; no installation or
`tests/__init__.py` is needed. Tests call the shipped `is_target_tcin` and
`is_bounded_json_tree`, not local replacement targets.

Coverage includes ASCII-eight/control rejection, native JSON/alias rejection,
one observation per direct call, prior-trace identity, three injected exception
types, subsequent recovery, pre-target exception identity, unrelated real calls,
empty operations, once-only side effects, supplied event-list preservation,
exact operation-result identity, unchanged fixtures, and captured empty streams.
The record identity test returns its operation's record, not the guard's boolean.
Every installed prior trace has an outer `finally` restoring the original trace.

## Independent external mutation protocol

Apply each replacement separately to `tests/real_call_probe.py` only, from the
same original baseline. The following JSON literals specify exact unique old/new
substrings, including indentation and final newlines. Each designated test must
fail by assertion, not an import/runtime error. None of these receipts exists yet.

| Mutation | Old JSON string | New JSON string | Killing test |
| --- | --- | --- | --- |
| Omit restoration | `"        sys.settrace(previous)\n"` | `"        pass\n"` | `test_restore_success` |
| Omit append | `"            events.append(\"call\")\n"` | `"            pass\n"` | `test_real_predicate_results_and_events` |
| Ignore all code identities | `"        if event == \"call\" and frame.f_code is target:\n"` | `"        if event == \"call\" and False:\n"` | `test_real_predicate_results_and_events` |
| Invoke twice | `"        return operation()\n"` | `"        operation()\n        return operation()\n"` | `test_operation_side_effects_once` |
| Swallow RuntimeError | `"        return operation()\n"` | `"        try:\n            return operation()\n        except RuntimeError:\n            return None\n"` | `test_injected_exceptions_restore_and_recover` |
| Deduplicate calls | `"            events.append(\"call\")\n"` | `"            if \"call\" not in events:\n                events.append(\"call\")\n"` | `test_each_call_observed_by_code_identity` |

Names above belong to `RealCallProbeTests`. The swallow mutant intentionally
violates the return contract; its behavioral kill must be the missing-exception
assertion, not a static diagnostic. The outer trace fixture isolates restoration
mutants even when assertions fail. Later receipts must include independent mutant
results, passing original/final baselines, and unchanged original source hashes.

## Pending external checks

Parent review must verify hashes, the exact three-path allowlist, complete bodies,
and actual total formatted code/test/document lines against the 399-line budget.
Do not trim tests or claim an estimate as a measured count. Independent paper
admission precedes any source authorization or new GitHub implementation task.

Required later tools are the external shell variables `PYTHON` (Python 3.11),
`RUFF`, and `BASEDPYRIGHT`, named as in `docs/TARGET_TCIN.md`; current
repository check commands are in `CONTRIBUTING.md`.
Run full formatting and isolated Ruff selection `E,F,W,I,UP,B,A,C4,SIM,RUF,ANN`
with Python 3.11 targeting. Run Basedpyright strict over the full package and
tests using external Python 3.11 configuration, without hidden exclusions or
weakened settings. Discover inherited 33 tests plus these tests without skips;
compile with an external cache and inspect the diff. All execution is pending.

## Explicit deferrals

Hostile-fixture and static-import-wiring helpers remain separate deferred support.
Record R01-R09 remain wholly unaccepted, with mandatory future WIRE consumer tests.
A future complete record paper must itself fit 399 lines and include every full
matrix helper not separately shipped. Module selection/order, late-invalid
 discard, and 64/65 limits remain deferred. #33 F01-F12, #29 D01-D04, page bounds,
private household, live Costco/Amazon/Target, and shared expense remain mandatory
pending work. Existing rejected papers are preserved.

No live data, private authentication, network, installs, provider changes,
publication, production seams, or implementation lease is included. Executed
gates, exact-head review, publication, and fresh merged verification require
accepted scope and subsequent explicit authorization.

## Adopted independent scope clarifications
A trace-callback exception disables tracing; finally reinstalls the saved hook.
Not chained means events are not forwarded; prior local traces on already-running
frames are not promised removed. Exception propagation assumes restoration
succeeds; restoration failure can supersede the operation or injection exception.
