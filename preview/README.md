# Transient mobile needs preview

Run from the repository root with an existing Python interpreter:

    python3 -m http.server 8000 --bind 127.0.0.1

Open http://127.0.0.1:8000/preview/ locally. No dependencies or build step.
For evidence runs, select a free local port instead of assuming 8000 is free.

The empty editor supports nonempty titles, explicit positive finite quantities,
Groceries and Other. Edit/remove needs and include/exclude them in the single
basket review. Both surfaces derive from one in-memory state with stable IDs.
Amount units are explicitly unspecified, each, pack, kg, g, lb, oz, L or mL.
Unspecified displays as “unit not specified”; no title-based inference or unit
conversion occurs. Fractional quantities remain valid. Optional package/size
intent is text bounded to 120 characters (before trimming), not product matching.
Legacy operation callers omitting unit/packageIntent get unspecified/empty;
explicit invalid units and non-string/overlong package intent are rejected.
Editing, basket inclusion/exclusion and removal preserve shared amount intent.
Undo removal in the needs surface restores only the most recently removed need,
exactly once, with its original ID, position, title, amount intent, category and
basket inclusion. A second removal replaces that recovery. Successful add/edit
or include/exclude changes discard it; invalid submissions and editor open/cancel
do not. There are no timers. Removal focuses Undo removal; restoration focuses
Review basket selections and both announce through the live status.
The production removeNeedWithRecovery/restoreRemovedNeed helpers bind recovery
to the exact post-removal state; stale/repeated recovery cannot overwrite newer
state or roll back nextId. Existing pure operation contracts remain unchanged.
Optional human-entered TCIN accepts only an exact string of 8 ASCII digits
(including leading zeros), or empty; no trimming, numeric coercion or Unicode digits.
Omitted TCIN defaults to empty for legacy callers. Edit can explicitly clear it;
edit/include/remove/undo preserve it with all amount/category fields.

Review included needs, then select Prepare handoff for plain copyable text in
stable need order: title, quantity/unit, package/size intent, TCIN (or “none”) and
category. TCIN as entered — not verified against Target. Intent is not a matched
product; no dietary-safety or availability claim. Users perform all lookup,
matching and purchase themselves. No product/search URLs or deep links are generated.
Copy is click-only; denied/unsupported clipboard selects text for manual copying
and reports failure honestly. Late clipboard results cannot label newer text copied.
Successful add/edit/include/remove/undo clears prepared text and copied status;
invalid submissions and editor open/cancel retain it. Empty baskets give an
explicit empty state with Copy disabled, not purchase instructions.
Reload deliberately clears all needs, TCINs, selections, handoff and undo history.
Nothing is persisted. User text is rendered with textContent, never interpreted as HTML.

Run real operation tests and syntax checks with an existing Node.js 22+:

    node --check preview/app.js
    node --check preview/test_app.mjs
    node --test preview/test_app.mjs

The test fixtures are synthetic. Browser acceptance must additionally exercise
empty → add (with/without TCIN) → edit → include → handoff → remove, exclusion,
invalid TCIN field error/focus, explicit TCIN clearing, reload,
text safety, keyboard focus, 44px targets and geometry at 320/390/768 CSS px.
Also verify middle-need removal/undo preserves position and basket amount fields,
repeated/stale undo, invalid versus successful intervening operations, second
removal, and reload clearing recovery. Use synthetic data only; emulation is not
physical iPhone/Android qualification. Exercise real DOM clipboard success,
permission failure, unsupported clipboard and late success/failure after a mutation
and a newer preparation; no stale text/status or delayed focus changes.
Inherited full Python tests, Ruff lint/format and strict Basedpyright still apply.

This is a local candidate foundation, not M0 or specification #63/#64 acceptance.
No sign-in, storage, service worker, offers, prices, stock, totals, approval,
retailer contact, verified retailer handoff, ordering, pickup or receipts are implemented.
This precursor does not claim A02/A06 acceptance; Lane A offer-source qualification
remains BLOCKED on B-RETAILER-ACCESS. Durable needs/TCIN persistence is future work.
Later flow steps
are descriptive text only, not actionable controls. Do not enter private data.
Independent exact-head review and parent verification precede any integration.
