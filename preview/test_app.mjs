import test from 'node:test';
import assert from 'node:assert/strict';
import {
  emptyState, validateNeed, addNeed, editNeed, removeNeed, includeNeed, basketNeeds,
  amountUnits, packageIntentLimit, formatNeed,
} from './app.js';

// Synthetic adversarial fixtures only; these are not household or retailer data.
const fields = { title: 'Synthetic need', quantity: 2, category: 'Groceries' };

test('empty state, trimmed title and both categories', () => {
  assert.deepEqual(emptyState(), { nextId: 1, needs: [] });
  assert.deepEqual(basketNeeds(emptyState()), []);
  for (const category of ['Groceries', 'Other']) {
    assert.deepEqual(validateNeed({ ...fields, title: '  Need  ', category }), {
      title: 'Need', quantity: 2, category, unit: 'unspecified', packageIntent: '',
    });
  }
});

test('reject empty/non-string title and explicit invalid quantities', () => {
  for (const title of ['', '  ', null, 12, undefined]) {
    assert.throws(() => addNeed(emptyState(), { ...fields, title }), /title/);
  }
  for (const quantity of [0, -1, NaN, Infinity, -Infinity, '', '2', null, undefined]) {
    assert.throws(() => addNeed(emptyState(), { ...fields, quantity }), /quantity/);
    assert.throws(() => editNeed(addNeed(emptyState(), fields), 1, { ...fields, quantity }));
  }
  assert.throws(() => validateNeed({ ...fields, category: 'Retailer' }), /Groceries or Other/);
  assert.equal(validateNeed({ ...fields, quantity: 0.25 }).quantity, 0.25);
});

test('add/edit/include/exclude/remove share stable immutable state and basket', () => {
  const original = emptyState();
  let state = addNeed(original, fields);
  state = addNeed(state, { ...fields, title: 'Other need', category: 'Other' });
  assert.equal(original.needs.length, 0);
  assert.deepEqual(state.needs.map(need => need.id), [1, 2]);
  assert.deepEqual(basketNeeds(state), []);
  const previous = state;
  state = includeNeed(state, 1, true);
  assert.equal(previous.needs[0].included, false);
  state = editNeed(state, 1, { title: 'Edited', quantity: 3, category: 'Other' });
  assert.deepEqual(basketNeeds(state), [state.needs[0]]);
  assert.deepEqual(state.needs[0], {
    id: 1, title: 'Edited', quantity: 3, category: 'Other', included: true,
    unit: 'unspecified', packageIntent: '',
  });
  state = includeNeed(state, 1, false);
  assert.deepEqual(basketNeeds(state), []);
  state = includeNeed(state, 1, true);
  state = removeNeed(state, 1);
  assert.deepEqual(basketNeeds(state), []);
  assert.equal(state.needs[0].id, 2);
  state = addNeed(state, fields);
  assert.equal(state.needs[1].id, 3);
});

test('missing identifiers and non-boolean selections fail without mutation', () => {
  const state = addNeed(emptyState(), fields);
  assert.throws(() => editNeed(state, 99, fields), /no longer exists/);
  assert.throws(() => removeNeed(state, 99), /no longer exists/);
  assert.throws(() => includeNeed(state, 99, true), /no longer exists/);
  assert.throws(() => includeNeed(state, 1, 'true'), /true or false/);
  assert.equal(state.needs.length, 1);
  assert.equal(state.needs[0].included, false);
});

test('malicious HTML remains literal data through editing and basket selection', () => {
  const title = '<img src=x onerror="globalThis.pwned=true"><script>alert(1)</script>';
  let state = addNeed(emptyState(), { ...fields, title });
  state = editNeed(state, 1, { ...fields, title, category: 'Other' });
  state = includeNeed(state, 1, true);
  assert.equal(state.needs[0].title, title);
  assert.equal(basketNeeds(state)[0].title, title);
  assert.equal(globalThis.pwned, undefined);
});

test('legacy defaults are honest, without inference from title or package', () => {
  const state = addNeed(emptyState(), { ...fields, title: '2 kg pack of cans' });
  assert.equal(state.needs[0].unit, 'unspecified');
  assert.equal(state.needs[0].packageIntent, '');
  assert.equal(formatNeed(state.needs[0]), '2 · unit not specified · Groceries');
  const valid = validateNeed({ ...fields, packageIntent: '  500 g bag  ' });
  assert.equal(valid.unit, 'unspecified');
  assert.equal(valid.packageIntent, '500 g bag');
  assert.equal(formatNeed(valid), '2 · unit not specified · package/size: 500 g bag · Groceries');
});

test('explicit units distinguish each, pack and fractional weight/volume in Other', () => {
  assert.deepEqual(amountUnits, ['unspecified', 'each', 'pack', 'kg', 'g', 'lb', 'oz', 'L', 'mL']);
  let state = emptyState();
  for (const unit of amountUnits) {
    const quantity = ['kg', 'g', 'lb', 'oz', 'L', 'mL'].includes(unit) ? 0.25 : 2;
    state = addNeed(state, { ...fields, unit, quantity, category: 'Other' });
    const need = state.needs.at(-1);
    assert.equal(need.unit, unit);
    assert.equal(need.quantity, quantity);
    assert.equal(need.category, 'Other');
    assert.equal(formatNeed(need), `${quantity} · ${unit === 'unspecified' ? 'unit not specified' : unit} · Other`);
  }
  assert.equal(state.needs.length, amountUnits.length);
  assert.deepEqual(basketNeeds(state), []);
  assert.notEqual(formatNeed(state.needs[1]), formatNeed(state.needs[2]));
});

test('amount editing/inclusion/exclusion/removal roundtrip keeps immutable identity', () => {
  const initial = addNeed(emptyState(), { ...fields, unit: 'pack', packageIntent: '6 each' });
  const selected = includeNeed(initial, 1, true);
  const edited = editNeed(selected, 1, {
    ...fields, quantity: 0.5, category: 'Other', unit: 'kg', packageIntent: '500 g bag',
  });
  assert.equal(edited.needs[0].id, 1);
  assert.equal(edited.nextId, 2);
  assert.equal(selected.needs[0].unit, 'pack');
  assert.equal(selected.needs[0].packageIntent, '6 each');
  assert.equal(initial.needs[0].included, false);
  assert.notEqual(selected.needs[0], edited.needs[0]);
  assert.strictEqual(basketNeeds(edited)[0], edited.needs[0]);
  assert.equal(formatNeed(basketNeeds(edited)[0]), '0.5 · kg · package/size: 500 g bag · Other');
  const excluded = includeNeed(edited, 1, false);
  assert.deepEqual(basketNeeds(excluded), []);
  assert.equal(excluded.needs[0].packageIntent, '500 g bag');
  const restored = includeNeed(excluded, 1, true);
  assert.equal(basketNeeds(restored)[0].unit, 'kg');
  assert.deepEqual(removeNeed(restored, 1).needs, []);
  assert.equal(restored.needs.length, 1);
});

test('invalid unit/package type or length rejects add/edit without mutation', () => {
  assert.equal(packageIntentLimit, 120);
  const state = includeNeed(addNeed(emptyState(), fields), 1, true);
  const snapshot = structuredClone(state);
  const invalids = [
    ...['', 'KG', 'packs', 'invalid', null, undefined, 2, {}, []].map(unit => ({ unit })),
    ...[null, undefined, 2, {}, [], 'x'.repeat(121), ' '.repeat(121)].map(packageIntent => ({ packageIntent })),
  ];
  for (const invalid of invalids) {
    const field = Object.hasOwn(invalid, 'unit') ? 'unit' : 'packageIntent';
    for (const operation of [() => addNeed(state, { ...fields, ...invalid }),
      () => editNeed(state, 1, { ...fields, ...invalid })]) {
      assert.throws(operation, error => error.field === field);
      assert.deepEqual(state, snapshot);
    }
  }
  assert.equal(validateNeed({ ...fields, packageIntent: 'x'.repeat(120) }).packageIntent.length, 120);
  assert.equal(validateNeed({ ...fields, packageIntent: '   ' }).packageIntent, '');
});

test('malicious package remains literal through real operations and formatter', () => {
  const packageIntent = '<img src=x onerror="globalThis.pwned=true"><script>alert(1)</script>';
  const initial = addNeed(emptyState(), { ...fields, unit: 'pack', packageIntent });
  const edited = editNeed(initial, 1, { ...fields, unit: 'each', packageIntent, category: 'Other' });
  const selected = includeNeed(edited, 1, true);
  assert.equal(basketNeeds(selected)[0].packageIntent, packageIntent);
  assert.equal(formatNeed(basketNeeds(selected)[0]), `2 · each · package/size: ${packageIntent} · Other`);
  assert.equal(initial.needs[0].unit, 'pack');
  assert.equal(globalThis.pwned, undefined);
});
