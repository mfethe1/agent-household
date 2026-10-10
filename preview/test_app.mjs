import test from 'node:test';
import assert from 'node:assert/strict';
import {
  emptyState, validateNeed, addNeed, editNeed, removeNeed, includeNeed, basketNeeds,
} from './app.js';

// Synthetic adversarial fixtures only; these are not household or retailer data.
const fields = { title: 'Synthetic need', quantity: 2, category: 'Groceries' };

test('empty state, trimmed title and both categories', () => {
  assert.deepEqual(emptyState(), { nextId: 1, needs: [] });
  assert.deepEqual(basketNeeds(emptyState()), []);
  for (const category of ['Groceries', 'Other']) {
    assert.deepEqual(validateNeed({ ...fields, title: '  Need  ', category }), {
      title: 'Need', quantity: 2, category,
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
  assert.deepEqual(state.needs[0], { id: 1, title: 'Edited', quantity: 3, category: 'Other', included: true });
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
