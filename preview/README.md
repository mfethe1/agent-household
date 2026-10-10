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
Reload deliberately clears all needs and selections. Nothing is persisted.
User text is rendered with textContent, never interpreted as HTML.

Run real operation tests and syntax checks with an existing Node.js 22+:

    node --check preview/app.js
    node --check preview/test_app.mjs
    node --test preview/test_app.mjs

The test fixtures are synthetic. Browser acceptance must additionally exercise
empty → add → edit → include → review → remove, exclusion, validation, reload,
text safety, keyboard focus, 44px targets and geometry at 320/390/768 CSS px.
Inherited full Python tests, Ruff lint/format and strict Basedpyright still apply.

This is a local candidate foundation, not M0 or specification #63/#64 acceptance.
No sign-in, storage, service worker, offers, prices, stock, totals, approval,
retailer handoff, ordering, pickup or receipts are implemented. Later flow steps
are descriptive text only, not actionable controls. Do not enter private data.
Independent exact-head review and parent verification precede any integration.
