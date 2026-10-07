# Goal prompt: Agent Household

## Mission
Build an open-source, agent-native household shopping and shared-expense system. Help users plan and prepare Costco, Amazon and Target purchases, retain grocery and restaurant receipts, and allocate costs accurately among consenting participants. Save users effort without surrendering control of purchases, sensitive data or shared debts.

This is an outcome contract, not a claim that integrations already work. Begin by reading README.md, docs/TRANSACTION_MODEL.md, docs/ACCEPTANCE.md and BACKLOG.md. Work in small, independently verifiable slices. Reuse qualified components instead of recreating meal planning, identity or accounting unnecessarily; inspect licenses before reuse.

## Required scope
- Costco, Amazon and Target are the required shopping retailers. Qualify channels separately: warehouse versus shipped versus same-day, and Amazon retail versus Fresh. Other retailers are optional, not dependencies.
- Grocery orders placed through the system and grocery purchases made elsewhere are receipt sources. Restaurant receipt capture and sharing are included; restaurant ordering is not.
- Agent/MCP interfaces and a phone-friendly visual review surface share one backend and one authorization model. A chat assistant must not become a second ledger.
- Offer self-hosted operation. Public repository contains generic code, documentation and clearly labeled synthetic fixtures only. Runtime household data stays private and outside Git.

## Resolve the high-risk dependencies first
1. Produce a per-retailer, per-channel capability matrix: discovery, product details, local price/availability, authenticated cart read/add/change/remove, checkout handoff, order status, itemized receipts and refunds. Record access requirements, source, verification time, supported geography, limits, license/terms constraints and evidence level: documented, source-inspected, live-tested or unavailable.
2. Prove a usable mobile checkout handoff for one retailer before building universal checkout. Browser automation is a fallback only when supported and explicitly authorized; never depend on exported cookies, borrowed credentials, evaded enrollment or undocumented access rights.
3. Qualify receipt access separately from shopping access. A linked account can expose itemized receipts, confirmations or only transactions. Show completeness rather than assuming itemization. Provide upload/manual correction fallback.
4. Specify transaction and expense lifecycles before implementing money-related features. Keep basket, order, shipment, receipt, charge, allocation and settlement separate but correlated.
5. Track external blockers as separate owned tasks. Integration failure must not block independent receipt-upload and expense-sharing work.

## Shopping contract
- Convert user-authorized needs, optional calendar context and receipt history into drafts. Attendance and dietary safety cannot be inferred from purchase history or calendar titles alone.
- Match exact variant, seller, pack, quantity and usable unit. Require current label evidence for hard dietary restrictions; uncertain labels block safety claims. No sensitive automatic substitutions.
- Compare whole baskets using merchandise, tax estimates, fees, tips, membership requirements, delivery/pickup availability, usable quantity, waste and user-selected convenience preferences. Mark estimates and unknowns; do not advertise an incomplete basket as cheapest.
- Keep preferences separate from approval: saved brands, split templates and fulfillment preferences reduce repeated questions but never authorize spending.
- Preserve user cart lines. Record agent-owned changes, detect concurrent user edits, and refresh before approval. Prevent concurrent restock requests from buying the same need twice.
- Approval binds user/account, retailer/channel, exact items/sellers/quantities, one-time purchase mode, substitution policy, fulfillment/slot, masked payment reference, total or approved ceiling and expiry. Material changes invalidate approval.
- Persist submission attempts before external action. Ambiguous outcomes become UNKNOWN; reconcile authoritative retailer history before retry. Never blindly repeat a purchase.
- Initial checkout can be user-completed. Unsupported native checkout remains explicitly unsupported. No surprise subscriptions or recurring purchases.

## Receipts and ingestion contract
- Preserve original evidence, provenance and version history. Extract merchant/date/currency, line items, discounts, taxes, tips, fees, subtotal, paid total and refunds with source references and uncertainty.
- Record owner/uploader, linked-account owner, actual payer(s) and participants separately. Never infer debt from uploading or group membership.
- Support images, digital receipts, multiple pages and explicitly authorized linked sources. Display last successful sync, historical coverage, completeness, expired authorization and failed imports.
- Handle duplicate uploads, import retries, order confirmations versus final receipts, revised receipts, multiple shipments/charges and partially fulfilled orders. Fuzzy duplicate matches require review; retain legitimate identical purchases.
- Restaurant support includes pre-tip/final receipts, split checks, shared dishes, service charges, discounts, cash, gift cards and multiple payers. Do not count both a service charge and tip as the same field.
- An uncertain or non-reconciling receipt stays a draft. Users can correct extraction without silently altering the original evidence. A receipt is not automatically proof of a settled payment.

## Shared-expense contract
- Support equal, percentage, fixed-amount and item-level splits; explicit shared-tax/tip/fee/discount allocation and multiple payers. Use integer currency minor units and deterministic rounding; never use floating-point amounts or implicit cross-currency netting.
- Distinguish proposed, accepted, disputed and settled obligations. Posting authority and consent are explicit. Default: a participant's obligation requires their acceptance; non-account participants remain provisional unless the operator has explicitly configured a consensual alternative.
- Provide guest identities, explicit claim/merge review and group join/leave rules. Shared retailer credentials do not imply shared visibility or financial responsibility.
- Settled expenses cannot be silently rewritten. Corrections and partial refunds create attributable adjustment entries; settlement reversal preserves history.
- Show who owes whom and explain every balance from source records. Recorded settlements track user-reported payment; they do not execute or prove a transfer. Actual payment processing, collections and external reminder messages are outside initial scope.
- Show retailer gross spending, budget-category spending, personal allocated cost, outstanding reimbursement and received reimbursement separately. Restaurant expenses are separately categorized by default.

## Product, privacy and recovery contract
- Phone-first flows: upload, extraction review, payer/participant selection, item assignment, basket approval, balances and exception resolution. Meet keyboard/accessibility requirements and preserve drafts across interrupted sessions.
- One source of truth for chat and UI, with actor-bound authorization, revision checks, idempotent mutations and correlated action receipts. Previewing a tool call must not execute it.
- Minimize data collection; separate tokens from receipt data; redact payment/account details from logs and exports. Encrypt stored sensitive data and backups, document key management and restore procedure, and test restoration.
- Group membership alone never reveals all receipts. Define owner/group/participant visibility and explicit sharing. Verify authorization server-side on every record and attachment access.
- Account unlinking stops new imports and revokes supported tokens. Publish a concrete retention/deletion policy before multi-user use: describe original-image deletion, minimal ledger retention, backups and member departure. Export before deletion when requested; do not claim data deleted while retained in backups without disclosure.
- Treat receipt text, retailer content and connector responses as untrusted data. They cannot authorize tools, purchases or policy changes. Upload validation must cover content type, size, malware risk and unsafe document parsing; OCR/model calls require disclosed data handling.
- Bound network retries and connector rate limits; show unavailable/stale states and manual recovery. Test crashes between external action and local confirmation.
- No production defaults containing sample debts, retailer credentials or fictional product availability. Synthetic fixtures are test-only and never evidence of a live integration.

## Delivery plan
Two tracks share the transaction model but proceed independently.
- Phase 0: capability research, lifecycle specification, threat model, visual contract, privacy boundary and prioritized acceptance matrix.
- Shopping track S1: one live-tested basket-to-mobile-handoff with approval and preserved carts; S2: other required retailers/channels; S3: cross-store comparison and order/receipt/refund reconciliation.
- Sharing track E1: retained photo/digital receipt plus user association, reconciliation and deduplication; E2: split review, consent and balances; E3: adjustments/refunds/settlement recording; E4: supported automatic ingestion and multi-user isolation.
- Release track R1: self-hosted installation, export/backup/restore, accessibility, operator guide and measurable pilot results. No public multi-tenant launch without independent security review.

## Execution and acceptance discipline
For each slice: state scope and invariants; inspect baseline; implement in an owned branch/worktree; run real tests, lint and type checks; obtain independent review for authorization, money, migrations and integration boundaries; verify exact artifact; then update backlog and evidence.

Do not weaken tests to get green, substitute mock retailer responses for live qualification, or report worker assertions as verification. Synthetic cases prove deterministic correctness; separately authorized private live cases prove retailer compatibility. Public evidence must be sanitized.

Every item has acceptance criteria, owner, dependency and status. Blocked items remain in progress with a separate unblock task. Finish a turn with DID / NEXT / NEED and verifiable evidence, not a promise. Publishing code does not establish product readiness.

Measure user effort saved against the same user's manual workflow. Report basket review time, receipt correction time, extraction discrepancies, match corrections, missing/duplicate imports, balance disagreements, handoff success and ongoing operating costs. Predeclare pilot thresholds in docs/ACCEPTANCE.md; do not claim savings from demos alone.

## First task for the executor
Produce an evidence-backed capability matrix and reviewed transaction/consent model. Turn all acceptance scenarios into dependency-ordered small tickets. Implement the local receipt-upload-to-reviewed-expense vertical slice while separately qualifying a retailer handoff. Do not request new subscriptions, connect accounts, invite participants, purchase products or transfer money without fresh action-specific operator authorization.
