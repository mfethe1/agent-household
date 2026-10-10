# Exact Target TCIN predicate

`agent_household.target_tcin.is_target_tcin(value: object) -> bool` accepts
exactly native strings of eight Unicode codepoints, each ASCII U+0030..U+0039.
Leading zeros are valid. Every result is an exact bool. Subclasses and other
objects are rejected before length, iteration, comparison or coercion callbacks.
The source uses exact-type short-circuiting, an eight-character length check,
and ASCII range comparisons. It performs no IO, logging, normalization, mutation,
document traversal, guard invocation or exception catching. Cancellation is not
caught; general hostile concurrent safety is not promised.

## Provenance

The exactly-eight-ASCII-digit length, and the canonical URL grammar in
`docs/TARGET_URL.md` that embeds it, have no recorded source or evidence level
(GOAL_PROMPT.md: documented, source-inspected, live-tested or unavailable) in
this repository. Both are unverified assumptions until the P0-01 capability
matrix (`docs/specs/SPEC-01.md`) records one; passing tests show only that the
code enforces them.

## Committed regression map

All test names below belong to `TargetTcinTests` in `tests/test_target_tcin.py`.

| Row | Concrete evidence |
| --- | --- |
| P01 | `test_valid_exact_strings_return_exact_true`: ordinary, zero, leading zero, nines; exact bool. |
| P02 | `test_every_length_edge_and_huge_string`: 0..7, 9..16, 100000. |
| P03 | `test_every_ascii_nondigit_at_every_position`: all U+0000..007F nondigits, all eight positions; named subTests. |
| P04 | `test_unicode_digits_confusables_and_surrogates`: named Unicode fixtures with escaped surrogates. |
| P05 | `test_nonstring_types_return_exact_false`: heterogeneous native and arbitrary objects. |
| P06 | `test_string_subclasses_rejected_even_with_valid_payload`; `test_hostile_fixtures_have_no_callbacks`: six counters, index-only fixture labels. |
| P07 | `test_valid_and_invalid_calls_are_silent`; `test_native_mutable_rejects_keep_identity_and_content`. |
| P08 | Static review of the entire predicate; external independent mutation protocol below. |
| P09 | External full inherited/new suite, strict gates, budget, hashes and exact-head review below. |

## External reproduction and acceptance

This section is the historical gate for this slice at the base named below,
which predates the `tests/` helper modules (`real_call_probe`,
`hostile_callbacks`); on later trees `extraPaths` of `[WORKTREE]` alone leaves
their imports unresolved. Current repository check commands are in
`CONTRIBUTING.md`.

This artifact reports no executed gates, mutation results, commits or review.
The parent installs only the three allowed new files; inherited files stay intact.
`WORKTREE` denotes the exclusively owned fresh checkout of admitted public main
`5c5f190cd9919c578ec2d1d967e333e1eca6515e`. `EVIDENCE` denotes an external
public-only evidence directory. Neither token denotes a committed config file.
`PYTHON`, `RUFF` and `BASEDPYRIGHT` are external shell variables resolving to the
adopted actual Python 3.11.14, Ruff 0.16.8 and Basedpyright 1.38.1 binaries.
Record each command's stdout, stderr and exit separately, including versions.

Before installation, run inherited discovery: require 24 tests and no skips.
Then run from `WORKTREE`, with no skipped tests or weakened diagnostics:

```sh
cd "$WORKTREE"
"$PYTHON" -B -m unittest discover -s tests -v
"$RUFF" check --isolated --no-cache --target-version py311 --select E,F,W,I,UP,B,A,C4,SIM,RUF,ANN agent_household tests
"$RUFF" format --isolated --check agent_household tests
"$BASEDPYRIGHT" --project "$EVIDENCE/pyrightconfig.json" --pythonpath "$PYTHON"
PYTHONPYCACHEPREFIX="$EVIDENCE/pycache" "$PYTHON" -m compileall -q agent_household tests
git diff --check
```

The external `EVIDENCE/pyrightconfig.json` must include absolute
`WORKTREE/agent_household` and `WORKTREE/tests`, set `extraPaths` to `[WORKTREE]`,
`pythonVersion` to `"3.11"`, and `typeCheckingMode` to `"strict"`; resolve tokens
before writing JSON. No exclusions or diagnostic overrides. Report inherited
or gate-profile failures separately; do not weaken the adopted profile.

## Independent mutation receipts

Use actual Python 3.11 and the original source to create four separate isolated
in-memory modules: remove the length check; replace exact type with `isinstance`;
replace the ASCII range with `character.isdigit()`; invert the predicate result.
For each module, load the committed test module and bind its imported
`is_target_tcin` name to that mutant, then run its complete unittest suite.
Require an assertion failure, not an import, setup, lint or runner failure.
Expected killing tests respectively are `test_every_length_edge_and_huge_string`,
`test_string_subclasses_rejected_even_with_valid_payload`,
`test_unicode_digits_confusables_and_surrogates`, and
`test_valid_exact_strings_return_exact_true`. Subclass admission must fail the
valid plain-subclass result assertion, not merely callback checks.
Record the original passing baseline, test counts and each assertion traceback
externally. Verify the original source hash unchanged and rerun the final baseline.
No production seam, disk mutation or unverified restoration claim is needed.

## Complete-candidate boundary

Before commit, measure additions plus deletions across the entire formatted
three-file diff against the exact fresh base, including initially untracked files.
Require exactly the allowed three new files and at most 399 changed lines.
Retain an oversized complete candidate uncommitted; never trim coverage, minify,
or partially commit. Record source/test/doc hashes and clean candidate commit.
External public-only transcripts, config, hashes and mutation receipts accompany
separate read-only exact-head review and independent real-gate reproduction.
Only the parent may publish after acceptance, then verify merged checkout gates
and hashes. The coding leaf has no filesystem execution or publication authority.

F01-F12 and D01-D04 remain pending, including F08 scanner integration and
F09-F12 scanner boundaries, mutation, cancellation and closure. P09 concerns
only this predicate. Issues #33/#29/#25/#23/#24 and private household,
Target/Amazon/Costco and shared-expense goals remain incomplete. This is neither
an adapter nor live integration, and predicate success closes no parent scope.
