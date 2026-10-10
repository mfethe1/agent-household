# Contributing

Start with GOAL_PROMPT.md and claim one bounded ticket before implementation. Work in an isolated branch/worktree; do not share mutable runtime databases or credentials.

Use real local persistence and discriminating tests. Synthetic fixtures must be clearly labeled and cannot establish live retailer compatibility. Never publish real receipts, account/order identifiers, credentials, household policies or calendars.

Run tests, lint, type checks and relevant end-to-end acceptance before proposing changes. Include exact commands/results, limitations, before/after visual evidence for UI changes, and a sanitized evidence summary. Authorization, money, migrations, public APIs and infrastructure changes require independent review. Keep pull requests small and coherent.

Do not bypass retailer authorization or claim undocumented consumer checkout support. Operator approval to publish this project is not permission to enroll users, connect accounts, spend money or send reminders.

Report suspected security issues privately to the repository maintainer rather than exposing user data in a public issue. A dedicated security disclosure channel must be established before a public hosted release.

## Running checks

Requires Python >= 3.11; code and tests use only the standard library. The lint and type-check tools are development-only, pinned in `requirements-dev.txt` and configured in `pyproject.toml`. From the repository root:

```sh
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -B -m unittest discover -s tests -v
ruff check .
ruff format --check .
basedpyright -p pyproject.toml
node --test preview/test_app.mjs   # Node.js 22+; see preview/README.md
```

Expected outcome: all tests pass with zero skips, and ruff and basedpyright report no diagnostics. Bare `python -m unittest` (without `discover -s tests`), dotted module paths such as `python -m unittest tests.test_real_call_probe`, and running from another directory are unsupported: the tests import `agent_household` from the current directory and sibling helpers through the path that `discover -s tests` sets up (docs/REAL_CALL_PROBE.md), and on Python 3.11 bare `python -m unittest` reports OK after running 0 tests. A `pyrightconfig.json` in the repository root or any parent directory overrides `pyproject.toml` for a bare `basedpyright` run, so always pass `-p pyproject.toml`.

CI (`.github/workflows/check.yml`) runs these commands on Python 3.11 and 3.13 for every pull request and every push to `main`, and fails if fewer than `MIN_TESTS` tests run or any test is skipped; raise `MIN_TESTS` in the change that adds tests. A green CI run on the exact head commit is the evidence for these gates. It does not replace the independent review required above.
