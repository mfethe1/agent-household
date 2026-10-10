export function validateNeed({ title, quantity, category }) {
  if (typeof title !== 'string' || !title.trim()) throw new Error('Enter a nonempty need title.');
  if (typeof quantity !== 'number' || !Number.isFinite(quantity) || quantity <= 0) {
    throw new Error('Enter an explicit positive finite quantity.');
  }
  if (!['Groceries', 'Other'].includes(category)) throw new Error('Choose Groceries or Other.');
  return { title: title.trim(), quantity, category };
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

export function basketNeeds(state) {
  return state.needs.filter(need => need.included);
}

export function mountPreview(document) {
  let state = emptyState();
  let editingId = null;
  const get = id => document.getElementById(id);
  const element = (tag, text) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const announce = text => { get('status').textContent = text; };
  const resetEditor = () => {
    editingId = null;
    get('need-form').reset();
    get('editor-heading').textContent = 'Add a need';
    get('submit').textContent = 'Add need';
    get('cancel').hidden = true;
    get('error').textContent = '';
    for (const id of ['title', 'quantity']) get(id).removeAttribute('aria-invalid');
  };
  const button = (text, action) => {
    const node = element('button', text);
    node.type = 'button';
    node.className = 'secondary';
    node.addEventListener('click', action);
    return node;
  };
  const render = () => {
    get('needs').replaceChildren();
    get('basket').replaceChildren();
    get('needs-empty').hidden = state.needs.length > 0;
    get('basket-empty').hidden = basketNeeds(state).length > 0;
    for (const need of state.needs) {
      const row = element('li');
      row.dataset.needId = String(need.id);
      row.append(element('h3', need.title), element('p', `${need.quantity} · ${need.category}`));
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
        for (const id of ['title', 'quantity', 'category']) get(id).value = need[id];
        get('editor-heading').textContent = 'Edit need';
        get('submit').textContent = 'Update need';
        get('cancel').hidden = false;
        get('title').focus();
      }), button('Remove', () => {
        state = removeNeed(state, need.id);
        if (editingId === need.id) resetEditor();
        render();
        get('title').focus();
        announce('Need removed from needs and basket.');
      }));
      row.append(label, actions);
      get('needs').append(row);
    }
    for (const need of basketNeeds(state)) {
      get('basket').append(element('li', `${need.title} — ${need.quantity} · ${need.category}`));
    }
  };
  get('need-form').addEventListener('submit', event => {
    event.preventDefault();
    try {
      const fields = {
        title: get('title').value,
        quantity: get('quantity').value.trim() ? Number(get('quantity').value) : NaN,
        category: get('category').value,
      };
      state = editingId === null ? addNeed(state, fields) : editNeed(state, editingId, fields);
      resetEditor();
      render();
      get('title').focus();
      announce('Need updated in this session only.');
    } catch (error) {
      get('error').textContent = error.message;
      const invalid = !get('title').value.trim() ? get('title') : get('quantity');
      invalid.setAttribute('aria-invalid', 'true');
      invalid.focus();
    }
  });
  get('cancel').addEventListener('click', () => { resetEditor(); get('title').focus(); });
  get('review').addEventListener('click', () => { get('basket-heading').focus(); });
  render();
}

if (typeof document !== 'undefined') mountPreview(document);
