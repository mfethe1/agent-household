# Agent Household

Open-source project specification for agent-assisted Costco, Amazon and Target shopping, grocery/restaurant receipt retention, and consent-based shared expenses.

**Status: specification stage.** This repository does not yet contain a shopping application, retailer connector, OCR service or shared-expense implementation. No retailer partnership or native checkout access is claimed.

## Start here
- [Goal prompt](GOAL_PROMPT.md): reusable execution contract for human/agent contributors.
- [Transaction model](docs/TRANSACTION_MODEL.md): proposed entities, transitions and financial invariants.
- [Acceptance scenarios](docs/ACCEPTANCE.md): required proof and pilot measurements.
- [Backlog](BACKLOG.md): dependency-ordered work and external blockers.
- [Contribution rules](CONTRIBUTING.md): evidence, privacy and review requirements.

## Intended experience
Plan needs → verify offers → review basket → approve exact purchase → retailer handoff → reconcile final receipt → propose shared costs → accept obligations → track adjustments and settlements.

Photo-based receipt sharing can be delivered independently of retailer integration. Linked-account ingestion is conditional on separately verified access. Settlement tracking is not money transfer.

## Privacy and project boundary
Never commit actual receipts, calendars, identities, account exports, browser profiles, tokens or production databases. Use clearly synthetic test fixtures. Private deployment evidence stays private; publish only sanitized summaries. Existing private household systems and their history are not included.

## License
MIT. Retailer trademarks belong to their owners; no endorsement is implied. Third-party integrations must satisfy their own access requirements and license/terms obligations.
