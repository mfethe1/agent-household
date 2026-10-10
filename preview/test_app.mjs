import test from 'node:test';
import assert from 'node:assert/strict';
import {
  emptyState, validateNeed, addNeed, editNeed, removeNeed, includeNeed, basketNeeds,
  amountUnits, packageIntentLimit, formatNeed, removeNeedWithRecovery, restoreRemovedNeed,
  formatHandoff, mountPreview,
} from './app.js';

// Synthetic adversarial fixtures only; these are not household or retailer data.
const fields = { title: 'Synthetic need', quantity: 2, category: 'Groceries' };

test('empty state, trimmed title and both categories', () => {
  assert.deepEqual(emptyState(), { nextId: 1, needs: [] });
  assert.deepEqual(basketNeeds(emptyState()), []);
  for (const category of ['Groceries', 'Other']) {
    assert.deepEqual(validateNeed({ ...fields, title: '  Need  ', category }), {
      title: 'Need', quantity: 2, category, unit: 'unspecified', packageIntent: '', tcin: '',
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
    unit: 'unspecified', packageIntent: '', tcin: '',
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

test('removal recovery restores all fields, position and basket once without ID rollback', () => {
  let original = emptyState();
  for (const title of ['First', '<script>synthetic()</script>', 'Last']) {
    original = addNeed(original, { ...fields, title, quantity: 0.25, unit: 'kg',
      packageIntent: '<img src=x onerror="synthetic()">', category: 'Other' });
  }
  original = includeNeed(original, 2, true);
  const snapshot = structuredClone(original);
  Object.freeze(original);
  Object.freeze(original.needs);
  original.needs.forEach(Object.freeze);
  const { state, recovery } = removeNeedWithRecovery(original, 2);
  assert.deepEqual(state.needs.map(need => need.id), [1, 3]);
  assert.deepEqual(basketNeeds(state), []);
  const removedSnapshot = structuredClone(state);
  const tokenSnapshot = structuredClone(recovery);
  const restored = restoreRemovedNeed(state, recovery);
  assert.deepEqual(restored, snapshot);
  assert.deepEqual(basketNeeds(restored), [snapshot.needs[1]]);
  assert.deepEqual(original, snapshot);
  assert.deepEqual(state, removedSnapshot);
  assert.deepEqual(recovery, tokenSnapshot);
  assert.strictEqual(restoreRemovedNeed(restored, recovery), restored);
  const added = addNeed(restored, fields);
  assert.deepEqual(added.needs.map(need => need.id), [1, 2, 3, 4]);
  assert.equal(added.nextId, 5);
  assert.strictEqual(restoreRemovedNeed(added, recovery), added);
  assert.strictEqual(restoreRemovedNeed(state, null), state);
});

test('second removal replaces recovery; older and repeated tokens cannot restore', () => {
  let original = addNeed(addNeed(addNeed(emptyState(), fields), fields), fields);
  original = includeNeed(original, 3, true);
  const first = removeNeedWithRecovery(original, 1);
  const second = removeNeedWithRecovery(first.state, 3);
  assert.strictEqual(restoreRemovedNeed(second.state, first.recovery), second.state);
  const restored = restoreRemovedNeed(second.state, second.recovery);
  assert.deepEqual(restored.needs.map(need => need.id), [2, 3]);
  assert.deepEqual(basketNeeds(restored).map(need => need.id), [3]);
  assert.strictEqual(restoreRemovedNeed(restored, first.recovery), restored);
  assert.strictEqual(restoreRemovedNeed(restored, second.recovery), restored);
  assert.equal(restored.nextId, 4);
});

test('invalid operations retain recovery, every successful mutation invalidates it', () => {
  const original = addNeed(addNeed(emptyState(), fields), fields);
  const { state, recovery } = removeNeedWithRecovery(original, 1);
  const snapshot = structuredClone(state);
  for (const operation of [
    () => addNeed(state, { ...fields, title: '' }),
    () => editNeed(state, 2, { ...fields, quantity: 0 }),
    () => editNeed(state, 2, { ...fields, unit: 'invalid' }),
    () => editNeed(state, 99, fields),
    () => includeNeed(state, 2, 'true'),
    () => includeNeed(state, 99, true),
    () => removeNeedWithRecovery(state, 99),
  ]) {
    assert.throws(operation);
    assert.deepEqual(state, snapshot);
    assert.deepEqual(restoreRemovedNeed(state, recovery), original);
  }
  for (const changed of [addNeed(state, fields), editNeed(state, 2, fields),
    includeNeed(state, 2, true), includeNeed(state, 2, false)]) {
    assert.strictEqual(restoreRemovedNeed(changed, recovery), changed);
    assert.ok(!changed.needs.some(need => need.id === 1));
  }
  assert.strictEqual(restoreRemovedNeed(emptyState(), recovery).needs.length, 0);
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

test('TCIN accepts only empty or exact eight ASCII digits without coercion', () => {
  for (const tcin of ['', '00000000', '01234567', '99999999']) {
    assert.equal(validateNeed({ ...fields, tcin }).tcin, tcin);
  }
  const hostile = { toString() { throw new Error('must not coerce'); } };
  for (const tcin of ['1234567', '123456789', '1234567x', '１２３４５６７８', '١٢٣٤٥٦٧٨',
    ' 12345678', '12345678 ', '12345678\n', '\n', 12345678, null, undefined, true,
    new String('12345678'), [], hostile]) {
    const state = addNeed(emptyState(), fields);
    for (const operation of [addNeed.bind(null, state), editNeed.bind(null, state, 1)]) {
      assert.throws(() => operation({ ...fields, tcin }), error => error.field === 'tcin');
      assert.equal(state.needs[0].tcin, '');
    }
  }
});

test('handoff has exact ordered included fields, literal intent, TCIN clearing and empty state', () => {
  const title = '<script>globalThis.pwned=true</script>';
  const bound = { ...fields, title, quantity: 0.5, unit: 'kg', category: 'Other',
    packageIntent: '<img src=x onerror=synthetic()>', tcin: '01234567' };
  let state = addNeed(addNeed(emptyState(), bound), { ...fields, title: 'Excluded' });
  state = addNeed(state, { ...fields, title: 'Last' });
  state = includeNeed(includeNeed(state, 3, true), 1, true);
  state = editNeed(state, 1, bound);
  assert.deepEqual(basketNeeds(state)[0], { ...bound, id: 1, included: true });
  assert.equal(formatHandoff(state), [
    'Basket needs — intent only, not matched products. No dietary-safety or availability claim.',
    'TCIN as entered — not verified against Target. You perform all lookup, matching and purchase yourself.',
    `${title} — 0.5 kg · package/size: ${bound.packageIntent} · TCIN: 01234567 · category: Other`,
    'Last — 2 unit not specified · package/size: none · TCIN: none · category: Groceries',
  ].join('\n'));
  const removed = removeNeedWithRecovery(state, 1);
  assert.deepEqual(restoreRemovedNeed(removed.state, removed.recovery), state);
  state = includeNeed(includeNeed(state, 1, false), 1, true);
  assert.equal(state.needs[0].tcin, '01234567');
  state = editNeed(state, 1, { ...bound, tcin: '' });
  assert.equal(state.needs[0].tcin, '');
  assert.ok(!formatHandoff(state).includes('01234567'));
  assert.equal(formatHandoff(emptyState()), 'No needs included. Nothing to hand off.');
  assert.equal(formatHandoff(addNeed(emptyState(), bound)), formatHandoff(emptyState()));
  assert.equal(globalThis.pwned, undefined);
});

// Minimal synthetic DOM adapter executes mountPreview, not a duplicated UI model.
function mounted(clipboard) {
  const nodes = new Map();
  const document = { defaultView: { navigator: { clipboard } },
    getElementById: id => nodes.get(id), createTextNode: text => ({ textContent: text }) };
  document.createElement = () => {
    const handlers = new Map();
    return { textContent: '', value: '', hidden: false, disabled: false, dataset: {}, children: [],
      attrs: new Map(), append(...children) { this.children.push(...children); },
      replaceChildren() { this.children = []; },
      setAttribute(key, value) { this.attrs.set(key, value); },
      removeAttribute(key) { this.attrs.delete(key); },
      addEventListener(type, action) { handlers.set(type, action); },
      emit(type) { return handlers.get(type)?.({ preventDefault() {} }); },
      focus() { document.activeElement = this; }, select() { this.selected = true; },
      querySelector(selector) {
        const row = this.children.find(child => child.dataset?.needId === selector.match(/"(\d+)"/)[1]);
        return row.children[2].children[0];
      },
    };
  };
  for (const id of ['title', 'quantity', 'category', 'unit', 'packageIntent', 'tcin', 'status',
    'error', 'need-form', 'editor-heading', 'submit', 'cancel', 'undo-removal', 'review',
    'needs', 'basket', 'needs-empty', 'basket-empty', 'basket-heading', 'prepare-handoff',
    'handoff', 'handoff-heading', 'handoff-text', 'copy-handoff']) nodes.set(id, document.createElement());
  const get = id => nodes.get(id);
  get('need-form').reset = () => {
    for (const id of ['title', 'quantity', 'packageIntent', 'tcin']) get(id).value = '';
    get('category').value = 'Groceries'; get('unit').value = 'unspecified';
  };
  get('need-form').reset();
  mountPreview(document);
  const submit = (values = fields) => {
    for (const [id, value] of Object.entries(values)) get(id).value = String(value);
    get('need-form').emit('submit');
  };
  const action = index => get('needs').children[0].children[3].children[index].emit('click');
  const include = () => {
    const checkbox = get('needs').children[0].children[2].children[0];
    checkbox.checked = !checkbox.checked; checkbox.emit('change');
  };
  return { get, document, submit, action, include, prepare: () => get('prepare-handoff').emit('click') };
}

test('mounted handoff invalidates on every mutation but not editor open/cancel or errors', async () => {
  const writes = [];
  const ui = mounted({ writeText: async text => { writes.push(text); } });
  const { get, submit, action, include, prepare } = ui;
  prepare();
  assert.equal(get('handoff-text').textContent, formatHandoff(emptyState()));
  assert.equal(get('copy-handoff').disabled, true);
  submit({ ...fields, tcin: '01234567' }); include(); prepare();
  assert.deepEqual(writes, []);
  await get('copy-handoff').emit('click');
  assert.deepEqual(writes, [get('handoff-text').textContent]);
  const copied = get('status').textContent;
  const text = get('handoff-text').textContent;
  action(0);
  assert.equal(get('tcin').value, '01234567');
  submit({ ...fields, tcin: 'bad' });
  assert.equal(get('tcin').attrs.get('aria-invalid'), 'true');
  assert.equal(ui.document.activeElement, get('tcin'));
  get('cancel').emit('click');
  assert.equal(get('handoff-text').textContent, text);
  assert.equal(get('status').textContent, copied);
  const invalidated = () => {
    assert.equal(get('handoff').hidden, true);
    assert.equal(get('handoff-text').textContent, '');
    assert.equal(get('copy-handoff').disabled, true);
    assert.ok(!get('status').textContent.includes('copied'));
    get('copy-handoff').emit('click');
    assert.deepEqual(writes, [text]);
  };
  action(0); submit({ ...fields, tcin: '' }); invalidated();
  prepare(); include(); invalidated();
  include(); prepare(); submit(fields); invalidated();
  prepare(); action(1); invalidated();
  prepare(); get('undo-removal').emit('click'); invalidated();
});

test('mounted clipboard fallback is honest and late completion cannot relabel newer handoff', async () => {
  for (const clipboard of [undefined, { writeText: async () => { throw new Error('denied'); } }]) {
    const ui = mounted(clipboard);
    ui.submit(); ui.include(); ui.prepare();
    await ui.get('copy-handoff').emit('click');
    assert.match(ui.get('status').textContent, /copy it manually/);
    assert.equal(ui.document.activeElement, ui.get('handoff-text'));
    assert.equal(ui.get('handoff-text').selected, true);
  }
  for (const fails of [false, true]) {
    let finish;
    const ui = mounted({ writeText: () => new Promise((resolve, reject) => {
      finish = () => fails ? reject(new Error('late denial')) : resolve();
    }) });
    ui.submit(); ui.include(); ui.prepare();
    const pending = ui.get('copy-handoff').emit('click');
    ui.submit(); ui.prepare();
    const status = ui.get('status').textContent;
    const focused = ui.document.activeElement;
    finish(); await pending;
    assert.equal(ui.get('status').textContent, status);
    assert.equal(ui.document.activeElement, focused);
    assert.equal(ui.get('copy-handoff').disabled, false);
  }
});
