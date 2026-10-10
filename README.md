# Agent Household

Open-source project specification for agent-assisted Costco, Amazon and Target shopping, grocery/restaurant receipt retention, and consent-based shared expenses.

**Status: specification stage.** The repository contains offline, standard-library-only development primitives in `agent_household/` with their tests, but no shopping application, retailer connector, OCR service or shared-expense implementation. No backlog ticket or acceptance item is complete. No retailer partnership or native checkout access is claimed.

## Start here
- [Goal prompt](GOAL_PROMPT.md): reusable execution contract for human/agent contributors.
- [Transaction model](docs/TRANSACTION_MODEL.md): proposed entities, transitions and financial invariants.
- [Acceptance scenarios](docs/ACCEPTANCE.md): required proof and pilot measurements.
- [Backlog](BACKLOG.md): dependency-ordered work, issue crosswalk, merged precursor work and external blockers.
- [Documentation index](docs/specs/INDEX.md): kind, origin and current status of every document under `docs/`.
- [Gap analysis](docs/reviews/2026-10-gap-analysis.md) and [remediation plan](docs/reviews/2026-10-remediation-plan.md): October 2026 audit, open owner decisions in #70.
- [Contribution rules](CONTRIBUTING.md): evidence, privacy and review requirements.

## Repository contents
- `agent_household/`: offline, fail-closed primitives (offer evidence arithmetic, bounded JSON tree guard, Target URL/TCIN/raw-title/module helpers). No network access, persistence or live retailer integration.
- `tests/`: `unittest` suite on synthetic inputs, plus test-support helpers.
- `docs/*.md`: transaction model, acceptance matrix and one module doc per primitive or test helper.
- `docs/specs/`: design papers and the documentation index.
- `docs/research/`: research briefs.
- `docs/reviews/`: audit reports.
- `preview/`: transient local mobile needs preview (no persistence, sign-in or retailer access); see `preview/README.md`.

## Running checks
Python 3.11 or newer; code and tests use only the standard library. From the repository root: `python3 -B -m unittest discover -s tests -v`. See [CONTRIBUTING.md](CONTRIBUTING.md) for lint, type-check and review requirements.

## Intended experience
Plan needs → verify offers → review basket → approve exact purchase → retailer handoff → reconcile final receipt → propose shared costs → accept obligations → track adjustments and settlements.

Photo-based receipt sharing can be delivered independently of retailer integration. Linked-account ingestion is conditional on separately verified access. Settlement tracking is not money transfer.

## Privacy and project boundary
Never commit actual receipts, calendars, identities, account exports, browser profiles, tokens or production databases. Use clearly synthetic test fixtures. Private deployment evidence stays private; publish only sanitized summaries. Existing private household systems and their history are not included.

## License
MIT. Retailer trademarks belong to their owners; no endorsement is implied. Third-party integrations must satisfy their own access requirements and license/terms obligations.
