# SPEC-01 Retailer Capability Matrix — Draft for #3

## 1. Status and scope
- Status: DRAFT — documented-evidence pass only; not reviewed; no cell is live-tested; requires independent review per #3.
- Date: 2026-10-10. Baseline: `main` @ `6f387c0`.
- Serves P0-01, A01 (`docs/ACCEPTANCE.md`), issue #3 and blocker B-RETAILER-ACCESS. Closes nothing; A01 stays PENDING; #3 and P0-01 stay OPEN.
- **Outcome of this pass: no first-party page could be fetched** (§8). Under §2 no cell is "documented", so every cell is UNKNOWN. §7 lists the candidate first-party sources that the next pass must fetch.
- No account was connected, no cart was read or changed and nothing was purchased. No partnership, program enrollment or retailer access is claimed.
- Required retailers: Costco, Amazon, Target (GOAL_PROMPT.md:9). Costco and Amazon channels follow GOAL_PROMPT.md:9.
- GOAL_PROMPT.md:9 does not enumerate Target channels. The Target rows below split fulfillment modes as #3 asks ("identify Target channel/store/fulfillment explicitly"). Their names are provisional, taken from an unfetched candidate (S14); the row set is owner decision O2.
- Instacart appears in §4 only because #66 raises it. It is optional, not required by GOAL, and not part of A01.
- This revision drafts the matrix, sources and qualification tasks only. §12 lists the #3 sections not yet drafted.

## 2. Evidence levels and notation
Levels (GOAL_PROMPT.md:15; A01):
- **documented**: a first-party page (retailer site, developer portal, help center or terms) fetched in a recorded session supports the cell. The cell cites its URL and access date.
- **source-inspected**: first-party source code or published schema inspected. Not used in this draft.
- **live-tested**: proved by a separately authorized private live case under B-RETAILER-ACCESS (GOAL_PROMPT.md:67). Not used in this draft.
- **unavailable**: a first-party source states the operation is not offered on that channel. Absence of a search hit is not "unavailable".
- **UNKNOWN**: none of the above. It is not a GOAL evidence level; it marks a cell not yet qualified.

A "documented" cell must also name the route its source documents:
- API: a documented programmatic interface.
- UI: the consumer site or app, used by a person.
- handoff: a link or form that sends the user to the retailer.

A UI route does not imply that an agent may automate it. GOAL_PROMPT.md:16 allows browser automation only as a fallback, when supported and explicitly authorized. Search-engine summaries and third-party pages are never evidence; they appear only in §9.

A01 also requires each cell to record access requirements, verification time, supported geography, limits and license/terms constraints. **None is established for any cell.** No cell has a verification time because none was verified. Fill these per cell when a source is fetched.

Columns (GOAL_PROMPT.md:15):

| Key | Operation |
|---|---|
| D | Discovery |
| P | Product details |
| L | Local price/availability |
| CR | Authenticated cart read |
| CA | Cart add |
| CC | Cart change |
| CX | Cart remove |
| H | Checkout handoff |
| O | Order status |
| R | Itemized receipts |
| F | Refunds |

## 3. Matrix — required retailers and channels
Each cell: evidence level [cell-note id, §5].

| Row | Retailer / channel | D | P | L | CR | CA | CC | CX | H | O | R | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CO-W | Costco warehouse | UNKNOWN [c1] | UNKNOWN [c1] | UNKNOWN [c1] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c4] | UNKNOWN [c4] | UNKNOWN [c4] |
| CO-S | Costco shipped (costco.com) | UNKNOWN [c1] | UNKNOWN [c1] | UNKNOWN [c1] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c2] | UNKNOWN [c5] | UNKNOWN [c5] | UNKNOWN [c5] |
| CO-D | Costco same-day | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] | UNKNOWN [c3] |
| AM-R | Amazon retail | UNKNOWN [a1] | UNKNOWN [a1] | UNKNOWN [a1] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a3] | UNKNOWN [a4] | UNKNOWN [a4] | UNKNOWN [a4] |
| AM-F | Amazon Fresh | UNKNOWN [a5] | UNKNOWN [a5] | UNKNOWN [a5] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a2] | UNKNOWN [a5] | UNKNOWN [a4] | UNKNOWN [a4] | UNKNOWN [a4] |
| TG-P | Target store pickup (provisional) | UNKNOWN [t1] | UNKNOWN [t1] | UNKNOWN [t2] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t4] | UNKNOWN [t4] | UNKNOWN [t4] |
| TG-U | Target Drive Up (provisional) | UNKNOWN [t1] | UNKNOWN [t1] | UNKNOWN [t2] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t4] | UNKNOWN [t4] | UNKNOWN [t4] |
| TG-D | Target same-day delivery (provisional) | UNKNOWN [t1] | UNKNOWN [t1] | UNKNOWN [t2] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t4] | UNKNOWN [t4] | UNKNOWN [t4] |
| TG-S | Target shipping (provisional) | UNKNOWN [t1] | UNKNOWN [t1] | UNKNOWN [t2] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t3] | UNKNOWN [t4] | UNKNOWN [t4] | UNKNOWN [t4] |

## 4. Optional — not required by GOAL (Instacart, per #66 only)
#66 distinguishes two Instacart routes; they are kept as separate rows.

| Row | Route | D | P | L | CR | CA | CC | CX | H | O | R | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IC-K | Instacart Developer Platform (API key) | UNKNOWN [i1] | UNKNOWN [i1] | UNKNOWN [i1] | UNKNOWN [i2] | UNKNOWN [i2] | UNKNOWN [i2] | UNKNOWN [i2] | UNKNOWN [i2] | UNKNOWN [i4] | UNKNOWN [i4] | UNKNOWN [i4] |
| IC-O | Instacart OAuth MCP (provisioned) | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] | UNKNOWN [i3] |

## 5. Cell notes
Every note shares one premise: no first-party page was fetched (§8). The S-ids are candidates (§7), not evidence.

**Costco**
- **c1**: Search found no Costco developer or API program page. That absence is not "unavailable". The terms candidate is S1.
- **c2**: No programmatic cart or handoff route was identified. Whether an agent may use the consumer site is a terms question (S1). For CO-W, whether cart and handoff apply to an in-person channel at all is owner decision O4.
- **c3**: The #66 comment (6084016798) records that Costco's FAQ (S2) confirms Same-Day is "powered by Instacart" with separate cart, member, address and markup constraints. That was not re-fetched here. Candidates: S2–S4. Overlap with the IC rows is owner decision O3.
- **c4**: Third-party leads (L6) say in-warehouse receipts appear in the member account. The only first-party candidate found is S5, a Canadian page. Whether O applies to in-person purchases is owner decision O4.
- **c5**: No first-party page was identified by search.

**Amazon**
- **a1**: Candidates S6–S8 (Creators API reference, PA-API 5 deprecation notice, migration guide). Whether any of them covers *local* price or availability is not established.
- **a2**: No programmatic cart route was identified. Terms candidate: S9, which #66 says "explicitly address[es] agents". Lead: L1.
- **a3**: Candidate S10, the PA-API 5 "Add to Cart form", found on a Japan-hosted copy. Its status after the PA-API 5 deprecation (S7; lead L3) is not established.
- **a4**: Search found no US first-party help page on order status, invoices or refunds, and no usable lead.
- **a5**: Candidate S11 covers Fresh eligibility and geography. Whether S6 covers Fresh items is not established.

**Target**
- **t1**: The #24 observation (§6) is identity-only and was not re-run, so it is not counted. A request to S12 was refused. Lead L4 (2014) says that portal is limited to employees and partners.
- **t2**: Blocked on #24. Price, stock and pickup-store identity are unqualified there.
- **t3**: Terms candidate: S13, whose URL was not confirmed. Lead L2 reports provisions admitting only "Agentic Commerce Agents" approved by the user and by Target.
- **t4**: No first-party page was identified. Lead: L8.

**Instacart (optional)**
- **i1**: #66 says the API-key platform documents shopping-list and recipe links. Search and price operations are not established. Candidates: S15–S17, S20.
- **i2**: The candidate route is a shopping-list link (S16–S17). #66 says it is "not autonomous order submission". Cart cells are UNKNOWN.
- **i3**: The #66 comment says the OAuth MCP "officially documents store availability, ingredient discovery and order assembly/modification/state". Access is "representative-provisioned", and the public docs "do not establish our entitlement, a final submit-order tool or Costco coverage". Candidates: S18, S19.
- **i4**: Not established.

## 6. Prior observation recorded in issues (not run in this pass)
#24 records the observation below. It is not counted as any evidence level:
- It was anonymous.
- It has no field-source map.
- It was not independently reviewed.
- #24 itself states that "an anonymous identity-only adapter cannot close this blocker or parent A01".

| Date | Operation | Channel / store | Result | Explicitly not qualified (#24) |
|---|---|---|---|---|
| 2026-10-08 | Anonymous Target product-detail GET, public TCIN 54602335 | none / none | HTTP 200; exact-TCIN title | seller/package fields, currency/pack price, pickup-store identity, pickup stock, complete labels |

## 7. Sources — candidate first-party pages (none fetched)
- "Found via" is either GitHub issue #66 or a WebSearch result on 2026-10-10.
- "Expected to cover" comes from #66 text or the search-result title. It is unverified and is not a paraphrase of fetched content.
- Every fetch attempt on 2026-10-10 was refused (§8).
- n/e: not established.
- Hosts on non-US domains are marked by country.

| ID | URL | Found via | Expected to cover (unverified) | Access date / result | Access requirements | Terms / license | Geography | Limits |
|---|---|---|---|---|---|---|---|---|
| S1 | https://costco.com/terms-and-conditions-of-use.html | search | Costco.com site terms | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S2 | https://customerservice.costco.com/app/answers/answer_view/a_id/8150/~/same-day-delivery-powered-by-instacart-faqs | #66 comment | Same-Day powered by Instacart; cart/member/address/markup constraints (#66) | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S3 | https://www.costco.com/same-day.html | search | Same-Day landing page | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S4 | https://costco.com/costco-grocery-faq.html | search | Grocery delivery FAQ | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S5 | https://costco.ca/costco-app.html | search | Costco app features | 2026-10-10 refused | n/e | n/e | Canada host | n/e |
| S6 | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference | search | Creators API operation reference | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S7 | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation | search | PA-API 5 deprecation notice | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S8 | https://affiliate-program.amazon.com/creatorsapi/docs/en-us/migrating-to-creatorsapi-from-paapi | search | PA-API → Creators API migration | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S9 | https://www.amazon.com/gp/help/customer/display.html?nodeId=GLSBYFE9MGKKQXXM | #66 comment | Conditions of Use; addresses agents (#66) | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S10 | https://webservices.amazon.co.jp/paapi5/documentation/add-to-cart-form.html | search | PA-API 5 "Add to Cart form" | 2026-10-10 refused | n/e | n/e | Japan host | n/e |
| S11 | https://aboutamazon.com/news/retail/amazon-expands-grocery-delivery-and-pickup | search | Grocery delivery/pickup announcement | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S12 | https://developer.target.com/ | search (named in L4) | Target developer portal | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S13 | target.com Terms and Conditions (URL not confirmed) | search (third-party copies only) | Target site terms, including agent provisions (per L2) | not attempted | n/e | n/e | n/e | n/e |
| S14 | https://corporate.target.com/about/shopping-experience/fulfillment-services | search | "Pickup & Delivery Services" (fulfillment modes) | 2026-10-10 refused | n/e | n/e | n/e | n/e |
| S15 | https://docs.instacart.com/developer_platform_api/guide/tutorials/mcp | #66 body | API-key MCP tutorial | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S16 | https://docs.instacart.com/developer_platform_api/guide/concepts/shopping_list | #66 body | Shopping-list page concept | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S17 | https://docs.instacart.com/developer_platform_api/api/products/create_shopping_list_page | search | "Create shopping list page" API reference | 2026-10-10 not attempted (host refused) | n/e | n/e | n/e | n/e |
| S18 | https://docs.instacart.com/mcp_servers | #66 comment | MCP servers overview | 2026-10-10 refused | representative-provisioned (#66, unverified) | n/e | n/e | n/e |
| S19 | https://docs.instacart.com/mcp_servers/get-started/use-instacarts-mcp-server | #66 comment | OAuth MCP usage | 2026-10-10 not attempted (host refused) | representative-provisioned (#66, unverified) | n/e | n/e | n/e |
| S20 | https://company.instacart.com/business/developers | search | Developer Platform program page | 2026-10-10 refused | n/e | n/e | n/e | n/e |

## 8. Fetch log (2026-10-10)
**Hosts refused.** This session's egress policy refused the HTTPS tunnel (HTTP 403) for these hosts, one request each:
- `docs.instacart.com`, `company.instacart.com`, `www.instacart.com`
- `customerservice.costco.com`, `www.costco.com`, `costco.com`, `costco.ca`
- `webservices.amazon.com`, `webservices.amazon.co.jp`, `www.amazon.com`, `affiliate-program.amazon.com`, `aboutamazon.com`
- `help.target.com`, `developer.target.com`, `www.target.com`, `corporate.target.com`

**Pages not attempted.** Individual pages on hosts already refused were not attempted; S13 has no confirmed URL.

**Other observations.**
- The WebFetch tool failed name resolution for `docs.instacart.com` and `customerservice.costco.com`.
- A control request to an unrelated allowed host succeeded.

**What this means.** The refusals are a property of this session's environment, not evidence about the retailers. Per the proxy rules, nothing was retried or routed around: no mirrors, archives or caches were used.

## 9. Unverified leads (third-party; never evidence)
Each lead must be checked against the first-party candidate in brackets before any use.

- **L1** [S9]: https://conductatlas.com/platform/amazon/amazon-conditions-of-use/agent-transparency-and-access-requirements/ claims Amazon's Conditions of Use contain agent terms: agents must identify themselves, and Amazon may limit or block agent access.
- **L2** [S13]: https://conductatlas.com/platform/target/target-terms-and-conditions/provision/CA-P-076752/only-target-approved-ai-agents-permitted/ claims Target's terms admit only "Agentic Commerce Agents" approved by the user and by Target.
- **L3** [S7]: https://dev.to/th3nate/amazon-pa-api-v5-is-shutting-down-april-30-2026-here-is-what-changes-at-the-auth-layer-22ek claims PA-API 5 shut down in 2026 in favor of the OAuth-based Creators API. Search results gave conflicting dates.
- **L4** [S12]: https://apievangelist.com/2014/10/09/the-publicly-available-private-target-apis/ (2014) says developer.target.com registration was limited to employees and trusted partners.
- **L5** [S18, S19]: https://agentman.ai/agentskills/connections/mcp-server/instacart says Instacart MCP rate limits are unpublished.
- **L6** [S5]: https://hip2save.com/2021/10/22/you-can-now-view-your-costco-receipts-online-in-the-app/ (2021) says in-warehouse receipts are viewable online and in the app.
- **L7** [S3, S4]: https://www.tastingtable.com/1812567/costco-shoppers-warn-against-same-day-delivery is consumer commentary on Costco same-day pricing.
- **L8** [none]: https://register.shoeboxed.com/blog/target-receipt claims target.com orders expose receipts and invoices, and that in-store purchases on a linked payment method appear in purchase history.

## 10. Open qualification tasks
**Q0. Documented pass (no account; prerequisite).** From an environment allowed to reach the §8 hosts:
- Fetch S1–S20. Record URL, access date, short paraphrase, access requirements, terms/license, geography and limits.
- Upgrade a cell only where a fetched first-party page supports it. Mark a cell unavailable only on an explicit first-party statement.
- Check leads L1–L3 first, because they decide whether any agent route is permitted at all.
- Search further for first-party pages for c4, c5, a4 and t4.

**B-RETAILER-ACCESS live tests, per row.** Ground rules for every row:
- Fresh, action-specific operator authorization (GOAL_PROMPT.md:74).
- The operator's own account, through a route the retailer's terms permit.
- No copied cookies, borrowed credentials or enrollment bypass (GOAL_PROMPT.md:16, #3).
- No purchase. Cart-mutation tests (CA/CC/CX) only under separate authorization.
- Record operation, channel, store, address scope and timestamp, with sanitized evidence.
- Record rate limits, retry bounds and stale or unavailable states (A25).
- An independent review comes before any cell is marked live-tested.

| Row | What must be tested live |
|---|---|
| CO-W | Price and stock for one named warehouse; any discovery route besides the consumer site; whether in-warehouse receipts are itemized in the member account; how returns appear. |
| CO-S | Address-specific price and availability; cart read; a user-completed phone checkout handoff (GOAL_PROMPT.md:16); order status; online-order receipt itemization; refund record. |
| CO-D | Which entry point reaches it (costco.com or Instacart); item price against warehouse price; whether its cart is separate from CO-S; handoff; whether order status, receipt and refund records sit with Costco or Instacart. |
| AM-R | Creators API eligibility and coverage of D, P and price/availability (S6–S8); whether the Add to Cart form (S10) still adds to the signed-in user's own cart for user-completed checkout; read-only order status and invoice; refund record. |
| AM-F | Whether any API or catalog route covers Fresh items and address-specific availability; whether Fresh has its own cart and delivery-window step in the handoff; whether Fresh pickup exists as a separate channel; estimated versus final charges for weighted items. |
| TG-P | For one named store, the fields #24 left unqualified: seller/package, currency/pack price, pickup-store identity, pickup stock, labels. Also handoff, order status, receipt and refund. |
| TG-U | Everything in TG-P, plus whether Drive Up is selected separately from pickup. |
| TG-D | Same-day eligibility by address; fees and membership; handoff; order status; receipt and refund record. |
| TG-S | Address-based availability; handoff; order status; receipt and refund record. |
| IC-K | Only if O1 adopts it: create a shopping-list link from a synthetic list with a development key (key issuance is enrollment, O5). Confirm the user-completed path and which store and price data the link exposes. |
| IC-O | Only if O1 and O5 approve: after provisioning, inspect the tool schema and store availability read-only; check whether a submit-order tool exists and whether Costco is covered. |

## 11. Owner decisions
- **O1. Instacart.** Does Instacart become a required channel or route? #66 asks for grocery-first Costco, Instacart and Amazon, but GOAL_PROMPT.md:9 keeps other retailers optional. If adopted, GOAL_PROMPT.md:9, A01 and this matrix change together.
- **O2. Target channel set.** GOAL does not enumerate Target channels.
  - Confirm rows TG-P, TG-U, TG-D and TG-S, and whether pickup and Drive Up are one channel.
  - `agent_household/offer_evidence.py` `channel` values are `warehouse`, `same_day`, `shipped`, `retail`, `fresh` and `pickup`. None names Drive Up, and nothing checks retailer/channel pairs (audit G46).
- **O3. Costco same-day.** Does a route through Instacart qualify CO-D? Can evidence from the IC rows be reused for CO-D?
- **O4. Warehouse (in-person) channel.** Which operations apply to it? Cart, handoff and order status may not apply. Until decided, those cells stay UNKNOWN, not "unavailable".
- **O5. Program enrollment.** Should the project apply for Amazon Associates / Creators API credentials, an Instacart Developer Platform key, or Instacart OAuth MCP provisioning?
  - Each needs fresh operator authorization (GOAL_PROMPT.md:74; #66 limits).
  - Each brings program terms that must be evaluated.
- **O6. Agent-terms posture.** If first-party terms confirm L1 or L2, does the product restrict those retailers to user-completed handoff? Who reviews retailer terms?
- **O7. Geography.** GOAL states no supported geography, and some candidates sit on Canadian and Japanese hosts (S5, S10). Choose the qualification geography.
- **O8. Vocabulary.** GOAL_PROMPT.md:15 and A01 use "unavailable" as an evidence level. #3 and GOAL_PROMPT.md:29 use "unsupported" for operations. This draft adds UNKNOWN as a placeholder that is not an evidence level. Confirm one shared vocabulary.
- **O9. Documented-pass environment.** Who runs Q0, and from what environment? Alternatively, should the §8 hosts be allowed for this agent environment?

## 12. Not drafted in this revision
Issue #3's final state also requires the following, which this revision does not draft:
- actors and stories
- scope and exclusions beyond §1
- resolved or blocked decisions beyond §11
- architecture contracts
- states and unknown/error behavior
- authorization and privacy boundaries
- dependency DAG
- Given/When/Then acceptance mapped to A01–A23 (#3), plus A24/A25 where they apply
- verification seams, authorized test procedures, recovery and compatibility
- a `docs/specs/TRACEABILITY.md` entry
- child implementation issues

Independent review of the exact revision is required before #3 or P0-01 can move.
