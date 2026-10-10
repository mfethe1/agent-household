export const amountUnits = ['unspecified', 'each', 'pack', 'kg', 'g', 'lb', 'oz', 'L', 'mL'];
export const packageIntentLimit = 120;

function invalidField(field, message) {
  throw Object.assign(new Error(message), { field });
}

export function validateNeed(fields) {
  const { title, quantity, category } = fields;
  const unit = Object.hasOwn(fields, 'unit') ? fields.unit : 'unspecified';
  const packageIntent = Object.hasOwn(fields, 'packageIntent') ? fields.packageIntent : '';
  if (typeof title !== 'string' || !title.trim()) invalidField('title', 'Enter a nonempty need title.');
  if (typeof quantity !== 'number' || !Number.isFinite(quantity) || quantity <= 0) {
    invalidField('quantity', 'Enter an explicit positive finite quantity.');
  }
  if (!['Groceries', 'Other'].includes(category)) invalidField('category', 'Choose Groceries or Other.');
  if (!amountUnits.includes(unit)) invalidField('unit', 'Choose a supported amount unit.');
  if (typeof packageIntent !== 'string' || packageIntent.length > packageIntentLimit) {
    invalidField('packageIntent', `Package/size intent must be text of at most ${packageIntentLimit} characters.`);
  }
  return { title: title.trim(), quantity, category, unit, packageIntent: packageIntent.trim() };
}

export function formatNeed(need) {
  const unit = need.unit === 'unspecified' ? 'unit not specified' : need.unit;
  const packageText = need.packageIntent ? ` · package/size: ${need.packageIntent}` : '';
  return `${need.quantity} · ${unit}${packageText} · ${need.category}`;
}

export function emptyState() {
  return { nextId: 1, needs: [] };
}

export function addNeed(state, fields) {
  const need = { ...validateNeed(fields), id: state.nextId, included: false };
  return { nextId: state.nextId + 1, needs: [...state.needs, need] };
}

function changeNeed(state, id, transform) {
  if (!state.needs.some(need => need.id === id)) throw new Error('Need no longer exists.');
  return { ...state, needs: state.needs.map(need => need.id === id ? transform(need) : need) };
}

export function editNeed(state, id, fields) {
  const valid = validateNeed(fields);
  return changeNeed(state, id, need => ({ ...need, ...valid }));
}

export function includeNeed(state, id, included) {
  if (typeof included !== 'boolean') throw new Error('Basket selection must be true or false.');
  return changeNeed(state, id, need => ({ ...need, included }));
}

export function removeNeed(state, id) {
  changeNeed(state, id, need => need);
  return { ...state, needs: state.needs.filter(need => need.id !== id) };
}

// Recovery is bound to the exact post-removal state, not stored in emptyState.
// Every successful add/edit/selection creates a new state and invalidates it.
export function removeNeedWithRecovery(state, id) {
  const next = removeNeed(state, id);
  const index = state.needs.findIndex(need => need.id === id);
  return { state: next, recovery: { state: next, index, need: { ...state.needs[index] } } };
}

export function restoreRemovedNeed(state, recovery) {
  if (!recovery || recovery.state !== state || state.needs.some(need => need.id === recovery.need.id)) {
    return state;
  }
  const needs = [...state.needs];
  needs.splice(recovery.index, 0, { ...recovery.need });
  return { ...state, needs };
}

export function basketNeeds(state) {
  return state.needs.filter(need => need.included);
}

export function mountPreview(document) {
  let state = emptyState();
  let editingId = null;
  let recovery = null;
  const get = id => document.getElementById(id);
  const element = (tag, text) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const announce = text => { get('status').textContent = text; };
  const fieldIds = ['title', 'quantity', 'category', 'unit', 'packageIntent'];
  const clearInvalid = () => {
    get('error').textContent = '';
    for (const id of fieldIds) get(id).removeAttribute('aria-invalid');
  };
  const resetEditor = () => {
    editingId = null;
    get('need-form').reset();
    get('editor-heading').textContent = 'Add a need';
    get('submit').textContent = 'Add need';
    get('cancel').hidden = true;
    clearInvalid();
  };
  const button = (text, action) => {
    const node = element('button', text);
    node.type = 'button';
    node.className = 'secondary';
    node.addEventListener('click', action);
    return node;
  };
  const render = () => {
    if (recovery?.state !== state) recovery = null;
    get('undo-removal').hidden = recovery === null;
    get('needs').replaceChildren();
    get('basket').replaceChildren();
    get('needs-empty').hidden = state.needs.length > 0;
    get('basket-empty').hidden = basketNeeds(state).length > 0;
    for (const need of state.needs) {
      const row = element('li');
      row.dataset.needId = String(need.id);
      row.append(element('h3', need.title), element('p', formatNeed(need)));
      const label = element('label');
      label.className = 'include';
      const checkbox = element('input');
      checkbox.type = 'checkbox';
      checkbox.checked = need.included;
      checkbox.setAttribute('aria-label', `Include ${need.title} in basket`);
      checkbox.addEventListener('change', () => {
        state = includeNeed(state, need.id, checkbox.checked);
        render();
        get('needs').querySelector(`[data-need-id="${need.id}"] input`).focus();
        announce('Basket selection updated.');
      });
      label.append(checkbox, document.createTextNode('Include in basket'));
      const actions = element('div');
      actions.className = 'actions';
      actions.append(button('Edit', () => {
        resetEditor();
        editingId = need.id;
        for (const id of fieldIds) get(id).value = need[id];
        get('editor-heading').textContent = 'Edit need';
        get('submit').textContent = 'Update need';
        get('cancel').hidden = false;
        get('title').focus();
      }), button('Remove', () => {
        ({ state, recovery } = removeNeedWithRecovery(state, need.id));
        if (editingId === need.id) resetEditor();
        render();
        get('undo-removal').focus();
        announce('Need removed from needs and basket. Undo removal is available until the next change.');
      }));
      row.append(label, actions);
      get('needs').append(row);
    }
    for (const need of basketNeeds(state)) {
      get('basket').append(element('li', `${need.title} — ${formatNeed(need)}`));
    }
  };
  get('need-form').addEventListener('submit', event => {
    event.preventDefault();
    clearInvalid();
    try {
      const fields = {
        title: get('title').value,
        quantity: get('quantity').value.trim() ? Number(get('quantity').value) : NaN,
        category: get('category').value,
        unit: get('unit').value,
        packageIntent: get('packageIntent').value,
      };
      state = editingId === null ? addNeed(state, fields) : editNeed(state, editingId, fields);
      resetEditor();
      render();
      get('title').focus();
      announce('Need updated in this session only.');
    } catch (error) {
      get('error').textContent = error.message;
      if (fieldIds.includes(error.field)) {
        const invalid = get(error.field);
        invalid.setAttribute('aria-invalid', 'true');
        invalid.focus();
      }
    }
  });
  for (const id of fieldIds) {
    get(id).addEventListener('input', clearInvalid);
    get(id).addEventListener('change', clearInvalid);
  }
  get('undo-removal').addEventListener('click', () => {
    const restored = restoreRemovedNeed(state, recovery);
    if (restored === state) return;
    state = restored;
    render();
    get('review').focus();
    announce('Need restored to its original position and basket selection. Changes are not saved.');
  });
  get('cancel').addEventListener('click', () => { resetEditor(); get('title').focus(); });
  get('review').addEventListener('click', () => { get('basket-heading').focus(); });
  render();
}

if (typeof document !== 'undefined') mountPreview(document);
