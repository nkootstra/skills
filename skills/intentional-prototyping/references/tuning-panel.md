# Tuning Panel

A dependency-free floating panel for dialing in values live. Copy the module below verbatim; the only thing that changes per prototype is the schema and the `onChange` binding. It stays identical across projects so it always reads as tooling, never as part of the design being judged. Do not restyle it with the project's tokens.

## Use an existing tool first

If the project already has a tuning library, use it instead of this module:

| Already in the project | Use |
| --- | --- |
| `dialkit` | DialKit (`useDialKit` / `createDialKit`); it also has spring, easing and timeline editors |
| `leva` | Leva's `useControls` |
| `tweakpane` | Tweakpane's `Pane` with `addBinding` |
| `lil-gui` / `dat.gui` | The existing GUI instance |

Do not add one of these as a dependency just for a prototype unless the user asks. This module exists so a single HTML file or a fresh sandbox can be tuned with zero installs.

## Rules

- **Bind every control to the real UI.** A slider that does not visibly change the thing being tuned is noise. Read `values` inside the render or animation code, not a copy taken at startup.
- **Preserve existing values as defaults.** If the component already uses `duration: 240`, the slider defaults to 240. Reset must return to what was there, not to a guess.
- **Choose useful ranges.** Wide enough to reach "clearly too much" on both sides, narrow enough that the useful zone is not a few pixels of slider travel. See [parameter-ranges.md](parameter-ranges.md).
- **Expose few controls.** Five to ten values that answer the prototype's question. Group by concern with key prefixes (`shadowBlur`, `shadowY`) rather than exposing everything.
- **Motion needs a replay.** If the tuned thing only animates on an event, add a `replay` toggle or a visible trigger next to it, so a change can be seen without hunting for the interaction.

## Schema

Keys become labels. The value's shape picks the control:

| Control | Schema | Value |
| --- | --- | --- |
| Slider | `duration: [240, 0, 1000, 10]` | `number`; tuple is `[default, min, max, step]`, step defaults to `(max - min) / 100` |
| Toggle | `bounce: true` | `boolean` |
| Select | `ease: { options: ['ease-out', 'ease-in-out'], default: 'ease-out' }` | one of `options`; `default` falls back to the first option |
| Color | `accent: '#0a84ff'` | hex string; must be `#rrggbb` to get a picker |
| Text | `label: 'Save'` | `string`; any non-hex string |

The numeric readout beside each slider is editable. Typing a value outside the slider range is allowed on purpose, for checking "what if it were 3000ms".

## API

```js
const tuner = createTuner(schema, onChange, options);
```

- `onChange(values, key)`: called on every input, once on creation (with `key` `null`), and after `set` / `reset`. `values` is the live object.
- `options.title`: panel heading, default `"Tune"`.
- `options.corner`: `'br' | 'bl' | 'tr' | 'tl'`, default `'br'`.
- `options.collapsed`: start collapsed.
- `options.render(el, values, index)`: enables the Variations button. Renders one instance into `el`; may return a cleanup function.
- `options.count`, `options.columns`: initial variation grid size (default 9 and 3).
- `options.vary`: keys to randomize in variations; default all. Pin the rest by leaving them out.

Returns:

- `tuner.values`: the live values object.
- `tuner.get(key?)`: one value, or a snapshot of all.
- `tuner.set(partial)`: update values and controls, then call `onChange`.
- `tuner.reset()`: back to defaults.
- `tuner.renderVariations(count, columns, renderFn)`: open the variations grid.
- `tuner.destroy()`: remove panel and grid.
- `tuner.el`: the panel element.

Behaviour: live update while dragging, no apply button. Reset and Copy JSON in the footer. The header collapses with the minus button or Escape. The arrow button (or double-clicking the header) moves the panel to the next corner; dragging the header places it anywhere. Every control is a native input with a label, so Tab, arrow keys and Space work. Light and dark follow `prefers-color-scheme`.

## Module

Paste into a `<script>` tag (it defines a global `createTuner`), or save as `tuner.js` with `export` before `function createTuner` and import it from a module script.

```js
function createTuner(schema, onChange = () => {}, options = {}) {
  const CSS = `
.tuner{--t-bg:rgba(255,255,255,.84);--t-fg:#1d1d1f;--t-muted:rgba(0,0,0,.5);--t-line:rgba(0,0,0,.08);--t-field:rgba(0,0,0,.05);--t-accent:#0a84ff;
  position:fixed;z-index:2147483646;width:248px;max-height:calc(100vh - 32px);display:flex;flex-direction:column;
  font:11px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--t-fg);background:var(--t-bg);
  -webkit-backdrop-filter:blur(14px) saturate(1.4);backdrop-filter:blur(14px) saturate(1.4);
  border:1px solid var(--t-line);border-radius:10px;box-shadow:0 1px 2px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.12);
  -webkit-font-smoothing:antialiased;user-select:none;-webkit-user-select:none;opacity:.94}
.tuner:hover,.tuner:focus-within{opacity:1}
@media (prefers-color-scheme:dark){.tuner{--t-bg:rgba(28,28,30,.84);--t-fg:#f5f5f7;--t-muted:rgba(255,255,255,.5);--t-line:rgba(255,255,255,.1);--t-field:rgba(255,255,255,.08);--t-accent:#0a84ff}}
.tuner[data-corner=br]{right:16px;bottom:16px}.tuner[data-corner=bl]{left:16px;bottom:16px}
.tuner[data-corner=tr]{right:16px;top:16px}.tuner[data-corner=tl]{left:16px;top:16px}
.tuner-head{display:flex;align-items:center;gap:2px;padding:4px 4px 4px 10px;cursor:grab;touch-action:none}
.tuner-head:active{cursor:grabbing}
.tuner-title{flex:1;font-weight:600;color:var(--t-muted);text-transform:uppercase;letter-spacing:.04em;font-size:10px}
.tuner button{font:inherit;color:inherit;background:none;border:0;border-radius:6px;padding:4px 7px;cursor:pointer}
.tuner button:hover{background:var(--t-field)}
.tuner :focus-visible{outline:2px solid var(--t-accent);outline-offset:1px}
.tuner-body{overflow:auto;padding:2px 10px 6px;border-top:1px solid var(--t-line)}
.tuner[data-collapsed] .tuner-body,.tuner[data-collapsed] .tuner-foot{display:none}
.tuner-row{display:grid;grid-template-columns:72px 1fr 44px;align-items:center;gap:6px;min-height:24px}
.tuner-row label{color:var(--t-muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tuner-row input[type=range]{width:100%;margin:0;accent-color:var(--t-accent)}
.tuner-row input[type=checkbox]{margin:0;justify-self:start;accent-color:var(--t-accent)}
.tuner-row select,.tuner-row input[type=text]{grid-column:2/4;font:inherit;color:inherit;background:var(--t-field);border:0;border-radius:5px;padding:3px 4px;min-width:0}
.tuner-row input[type=color]{width:100%;height:18px;padding:0;border:0;background:none;cursor:pointer}
.tuner-num{font:inherit;font-variant-numeric:tabular-nums;text-align:right;color:inherit;background:transparent;border:0;border-radius:4px;padding:2px 3px;width:100%;min-width:0;-moz-appearance:textfield}
.tuner-num:hover,.tuner-num:focus{background:var(--t-field)}
.tuner-num::-webkit-inner-spin-button,.tuner-num::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
.tuner-out{font-variant-numeric:tabular-nums;text-align:right;color:var(--t-muted)}
.tuner-foot{display:flex;flex-wrap:wrap;gap:2px;padding:4px;border-top:1px solid var(--t-line)}
.tuner-foot .tuner-var{display:flex;align-items:center;gap:2px;margin-left:auto;color:var(--t-muted)}
.tuner-foot .tuner-var input{width:30px}
.tuner-grid{position:fixed;inset:0;z-index:2147483645;overflow:auto;padding:16px;background:Canvas;color:CanvasText;font:11px/1.3 system-ui,-apple-system,"Segoe UI",sans-serif}
.tuner-grid-bar{display:flex;gap:8px;margin-bottom:12px}
.tuner-grid-bar button{font:inherit;padding:4px 10px;border-radius:6px;border:1px solid rgba(127,127,127,.3);background:none;color:inherit;cursor:pointer}
.tuner-tiles{display:grid;gap:12px}
.tuner-tile{position:relative;display:flex;flex-direction:column;border:1px solid rgba(127,127,127,.25);border-radius:8px;overflow:hidden;cursor:pointer}
.tuner-tile:hover{border-color:rgba(127,127,127,.6)}
.tuner-tile:focus-visible{outline:2px solid #0a84ff;outline-offset:2px}
.tuner-stage{position:relative;flex:1;min-height:160px;display:grid;place-items:center;overflow:hidden}
.tuner-caption{padding:6px 8px;font-variant-numeric:tabular-nums;opacity:.6;border-top:1px solid rgba(127,127,127,.2);white-space:normal}
`;

  const decimals = (step) => {
    const s = String(step);
    return s.includes('.') ? s.length - s.indexOf('.') - 1 : 0;
  };
  const kindOf = (spec) => {
    if (Array.isArray(spec)) return 'slider';
    if (typeof spec === 'boolean') return 'toggle';
    if (spec && Array.isArray(spec.options)) return 'select';
    if (typeof spec === 'string') return /^#[0-9a-f]{6}$/i.test(spec) ? 'color' : 'text';
    throw new Error('createTuner: unsupported control ' + JSON.stringify(spec));
  };
  const defaultOf = (spec) => {
    const kind = kindOf(spec);
    if (kind === 'slider') return spec[0];
    if (kind === 'select') return 'default' in spec ? spec.default : spec.options[0];
    return spec;
  };
  const stepOf = (spec) => spec[3] ?? +((spec[2] - spec[1]) / 100).toPrecision(2);
  const snap = (value, spec) => {
    const [, min, max] = spec;
    const step = stepOf(spec);
    const n = Math.round((Math.min(max, Math.max(min, value)) - min) / step) * step + min;
    return +n.toFixed(decimals(step));
  };
  const format = (value, spec) => Number(value).toFixed(decimals(stepOf(spec)));
  const randomOf = (spec, current) => {
    const kind = kindOf(spec);
    if (kind === 'slider') return snap(spec[1] + Math.random() * (spec[2] - spec[1]), spec);
    if (kind === 'toggle') return Math.random() < 0.5;
    if (kind === 'select') return spec.options[Math.floor(Math.random() * spec.options.length)];
    return current;
  };
  const el = (tag, props = {}, children = []) => {
    const node = Object.assign(document.createElement(tag), props);
    node.append(...children);
    return node;
  };

  if (!document.getElementById('tuner-style')) {
    document.head.append(el('style', { id: 'tuner-style', textContent: CSS }));
  }

  const keys = Object.keys(schema);
  const defaults = Object.fromEntries(keys.map((k) => [k, defaultOf(schema[k])]));
  const values = { ...defaults };
  const controls = {};
  const uid = Math.random().toString(36).slice(2, 7);

  const emit = (key) => onChange(values, key);

  // Panel shell
  const root = el('section', { className: 'tuner' });
  root.setAttribute('aria-label', options.title || 'Tuning panel');
  root.dataset.corner = options.corner || 'br';

  const title = el('span', { className: 'tuner-title', textContent: options.title || 'Tune' });
  const cornerBtn = el('button', { type: 'button', textContent: '⇲', title: 'Move to next corner (double-click header)' });
  cornerBtn.setAttribute('aria-label', 'Move panel to next corner');
  const collapseBtn = el('button', { type: 'button', textContent: '−' });
  collapseBtn.setAttribute('aria-label', 'Collapse panel');
  collapseBtn.setAttribute('aria-expanded', 'true');
  const head = el('div', { className: 'tuner-head' }, [title, cornerBtn, collapseBtn]);
  const body = el('div', { className: 'tuner-body' });
  body.id = 'tuner-body-' + uid;
  collapseBtn.setAttribute('aria-controls', body.id);

  // Rows
  for (const key of keys) {
    const spec = schema[key];
    const kind = kindOf(spec);
    const id = `tuner-${uid}-${key}`;
    const label = el('label', { htmlFor: id, textContent: key, title: key });
    const row = el('div', { className: 'tuner-row' }, [label]);
    let input;
    let readout = null;

    if (kind === 'slider') {
      const [, min, max] = spec;
      const step = stepOf(spec);
      input = el('input', { type: 'range', id, min, max, step, value: values[key] });
      readout = el('input', { type: 'number', className: 'tuner-num', min, max, step, value: format(values[key], spec) });
      readout.setAttribute('aria-label', key + ' value');
      input.addEventListener('input', () => {
        values[key] = snap(+input.value, spec);
        readout.value = format(values[key], spec);
        emit(key);
      });
      readout.addEventListener('change', () => {
        if (readout.value === '' || isNaN(+readout.value)) return (readout.value = format(values[key], spec));
        // Typed values may exceed the slider range on purpose; only snap to step.
        const typed = +readout.value;
        values[key] = typed < min || typed > max ? typed : snap(typed, spec);
        input.value = values[key];
        readout.value = format(values[key], spec);
        emit(key);
      });
      row.append(input, readout);
    } else if (kind === 'toggle') {
      input = el('input', { type: 'checkbox', id, checked: values[key] });
      readout = el('span', { className: 'tuner-out', textContent: values[key] ? 'on' : 'off' });
      input.addEventListener('change', () => {
        values[key] = input.checked;
        readout.textContent = input.checked ? 'on' : 'off';
        emit(key);
      });
      row.append(input, readout);
    } else if (kind === 'select') {
      input = el('select', { id }, spec.options.map((o) => el('option', { value: o, textContent: o })));
      input.value = values[key];
      input.addEventListener('change', () => {
        const match = spec.options.find((o) => String(o) === input.value);
        values[key] = match === undefined ? input.value : match;
        emit(key);
      });
      row.append(input);
    } else if (kind === 'color') {
      input = el('input', { type: 'color', id, value: values[key] });
      readout = el('span', { className: 'tuner-out', textContent: values[key] });
      input.addEventListener('input', () => {
        values[key] = input.value;
        readout.textContent = input.value;
        emit(key);
      });
      row.append(input, readout);
    } else {
      input = el('input', { type: 'text', id, value: values[key], spellcheck: false });
      input.addEventListener('input', () => {
        values[key] = input.value;
        emit(key);
      });
      row.append(input);
    }

    controls[key] = { kind, spec, input, readout };
    body.append(row);
  }

  const sync = (key) => {
    const { kind, spec, input, readout } = controls[key];
    const v = values[key];
    if (kind === 'slider') {
      input.value = v;
      readout.value = format(v, spec);
    } else if (kind === 'toggle') {
      input.checked = v;
      readout.textContent = v ? 'on' : 'off';
    } else {
      input.value = v;
      if (readout) readout.textContent = v;
    }
  };

  // Footer
  const resetBtn = el('button', { type: 'button', textContent: 'Reset' });
  const copyBtn = el('button', { type: 'button', textContent: 'Copy JSON' });
  const foot = el('div', { className: 'tuner-foot' }, [resetBtn, copyBtn]);

  let variationCount = options.count || 9;
  let variationColumns = options.columns || 3;
  if (options.render) {
    const countInput = el('input', { type: 'number', className: 'tuner-num', min: 1, max: 64, value: variationCount });
    const colsInput = el('input', { type: 'number', className: 'tuner-num', min: 1, max: 8, value: variationColumns });
    countInput.setAttribute('aria-label', 'Variation count');
    colsInput.setAttribute('aria-label', 'Variation columns');
    countInput.addEventListener('change', () => (variationCount = Math.max(1, +countInput.value || 1)));
    colsInput.addEventListener('change', () => (variationColumns = Math.max(1, +colsInput.value || 1)));
    const varBtn = el('button', { type: 'button', textContent: 'Variations' });
    varBtn.addEventListener('click', () => tuner.renderVariations(variationCount, variationColumns, options.render));
    foot.append(el('span', { className: 'tuner-var' }, [varBtn, countInput, '×', colsInput]));
  }

  resetBtn.addEventListener('click', () => tuner.reset());
  copyBtn.addEventListener('click', async () => {
    const text = JSON.stringify(values, null, 2);
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const area = el('textarea', { value: text });
      document.body.append(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    copyBtn.textContent = 'Copied';
    setTimeout(() => (copyBtn.textContent = 'Copy JSON'), 1200);
  });

  // Collapse, corners, drag
  const setCollapsed = (collapsed) => {
    root.toggleAttribute('data-collapsed', collapsed);
    collapseBtn.textContent = collapsed ? '+' : '−';
    collapseBtn.setAttribute('aria-expanded', String(!collapsed));
    collapseBtn.setAttribute('aria-label', collapsed ? 'Expand panel' : 'Collapse panel');
  };
  collapseBtn.addEventListener('click', () => setCollapsed(!root.hasAttribute('data-collapsed')));
  root.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      setCollapsed(true);
      collapseBtn.focus();
    }
  });

  const corners = ['br', 'bl', 'tl', 'tr'];
  const toCorner = (corner) => {
    root.style.left = root.style.top = root.style.right = root.style.bottom = '';
    root.dataset.corner = corner;
  };
  cornerBtn.addEventListener('click', () => {
    toCorner(corners[(corners.indexOf(root.dataset.corner) + 1) % corners.length] || 'br');
  });
  head.addEventListener('dblclick', (e) => {
    if (e.target === head || e.target === title) cornerBtn.click();
  });

  head.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 || e.target.closest('button')) return;
    const rect = root.getBoundingClientRect();
    const dx = e.clientX - rect.left;
    const dy = e.clientY - rect.top;
    head.setPointerCapture(e.pointerId);
    const move = (ev) => {
      const x = Math.min(window.innerWidth - rect.width, Math.max(0, ev.clientX - dx));
      const y = Math.min(window.innerHeight - 32, Math.max(0, ev.clientY - dy));
      root.removeAttribute('data-corner');
      Object.assign(root.style, { left: x + 'px', top: y + 'px', right: 'auto', bottom: 'auto' });
    };
    const up = () => {
      head.removeEventListener('pointermove', move);
      head.removeEventListener('pointerup', up);
      head.removeEventListener('pointercancel', up);
    };
    head.addEventListener('pointermove', move);
    head.addEventListener('pointerup', up);
    head.addEventListener('pointercancel', up);
  });

  root.append(head, body, foot);
  document.body.append(root);
  if (options.collapsed) setCollapsed(true);

  // Variations grid
  let grid = null;
  let cleanups = [];
  const closeGrid = () => {
    cleanups.forEach((fn) => typeof fn === 'function' && fn());
    cleanups = [];
    if (grid) grid.remove();
    grid = null;
  };
  const caption = (v) =>
    keys
      .filter((k) => ['slider', 'toggle', 'select'].includes(controls[k].kind))
      .map((k) => `${k} ${controls[k].kind === 'slider' ? format(v[k], schema[k]) : controls[k].kind === 'toggle' ? (v[k] ? 'on' : 'off') : v[k]}`)
      .join(' · ');

  const tuner = {
    values,
    get(key) {
      return key ? values[key] : { ...values };
    },
    set(partial) {
      for (const key of Object.keys(partial)) {
        if (!(key in controls)) continue;
        values[key] = partial[key];
        sync(key);
      }
      emit(null);
    },
    reset() {
      tuner.set(defaults);
    },
    renderVariations(count = variationCount, columns = variationColumns, renderFn = options.render) {
      if (!renderFn) throw new Error('renderVariations: pass a render function');
      closeGrid();
      const vary = options.vary || keys;
      const tiles = el('div', { className: 'tuner-tiles' });
      tiles.style.gridTemplateColumns = `repeat(${columns}, minmax(0, 1fr))`;
      const shuffleBtn = el('button', { type: 'button', textContent: 'Shuffle' });
      const closeBtn = el('button', { type: 'button', textContent: 'Close (Esc)' });
      shuffleBtn.addEventListener('click', () => tuner.renderVariations(count, columns, renderFn));
      closeBtn.addEventListener('click', closeGrid);
      grid = el('div', { className: 'tuner-grid' }, [el('div', { className: 'tuner-grid-bar' }, [shuffleBtn, closeBtn]), tiles]);
      grid.setAttribute('role', 'dialog');
      grid.setAttribute('aria-label', 'Variations');
      grid.addEventListener('keydown', (e) => e.key === 'Escape' && closeGrid());
      document.body.append(grid);

      for (let i = 0; i < count; i++) {
        const v = { ...values };
        for (const key of vary) v[key] = randomOf(schema[key], values[key]);
        const stage = el('div', { className: 'tuner-stage' });
        const tile = el('div', { className: 'tuner-tile', tabIndex: 0 }, [stage, el('div', { className: 'tuner-caption', textContent: caption(v) })]);
        tile.setAttribute('role', 'button');
        tile.setAttribute('aria-label', 'Load variation: ' + caption(v));
        const load = () => {
          closeGrid();
          tuner.set(v);
        };
        tile.addEventListener('click', load);
        tile.addEventListener('keydown', (e) => {
          if (e.target === tile && (e.key === 'Enter' || e.key === ' ')) {
            e.preventDefault();
            load();
          }
        });
        tiles.append(tile);
        cleanups.push(renderFn(stage, v, i));
      }
      shuffleBtn.focus();
    },
    destroy() {
      closeGrid();
      root.remove();
    },
    el: root,
  };

  emit(null);
  return tuner;
}
```

## Wiring example

Tuning a press interaction on a card. The panel only writes values; the card reads them every time it animates.

```html
<div class="card" id="card"></div>
<script type="module">
  import { createTuner } from './tuner.js';
  const card = document.getElementById('card');

  const tuner = createTuner(
    {
      pressScale: [0.97, 0.85, 1, 0.005],
      duration: [160, 0, 600, 10],
      ease: { options: ['cubic-bezier(0.23, 1, 0.32, 1)', 'cubic-bezier(0.77, 0, 0.175, 1)', 'ease'] },
      radius: [16, 0, 40, 1],
      shadow: true,
      color: '#f2f2f2',
    },
    (v) => {
      card.style.transition = `transform ${v.duration}ms ${v.ease}`;
      card.style.borderRadius = v.radius + 'px';
      card.style.background = v.color;
      card.style.boxShadow = v.shadow ? '0 1px 2px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.08)' : 'none';
    },
    {
      // Each tile gets its own instance with randomized values.
      render(el, v) {
        const tile = document.createElement('div');
        Object.assign(tile.style, {
          width: '120px',
          height: '80px',
          borderRadius: v.radius + 'px',
          background: v.color,
          transform: `scale(${v.pressScale})`,
          transition: `transform ${v.duration}ms ${v.ease}`,
        });
        el.append(tile);
      },
    },
  );

  card.addEventListener('pointerdown', () => (card.style.transform = `scale(${tuner.values.pressScale})`));
  card.addEventListener('pointerup', () => (card.style.transform = ''));
  card.addEventListener('pointerleave', () => (card.style.transform = ''));
</script>
```

## Variations

`renderVariations(count, columns, renderFn)` opens a full-screen grid beneath the panel. Each tile randomizes every key in `options.vary` within its range (numbers snap to step, toggles flip a coin, selects pick an option; colors and text keep their current value) and is labelled with its values. Click a tile, or focus it and press Enter, to load its values into the panel and close the grid. Shuffle rerolls; Escape closes. Count and columns are editable in the panel footer.

Use it when exploring, not when refining: it surfaces combinations nobody reaches by moving one slider at a time. Once a tile looks right, load it, then fine-tune with the sliders. Render tiles in their resting state, or render the state that matters (e.g. pressed), so differences are visible without interaction.

## React

The hook wraps the same module, so behaviour is identical. Save the module as `tuner.js` with `export` added, and the hook below as `useTuner.jsx` (or `useTuner.tsx` with types added in a TypeScript project):

```jsx
import { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { createTuner } from './tuner.js';

const defaultsOf = (schema) =>
  Object.fromEntries(
    Object.entries(schema).map(([key, spec]) => [
      key,
      Array.isArray(spec) ? spec[0] : spec && Array.isArray(spec.options) ? spec.default ?? spec.options[0] : spec,
    ]),
  );

// The schema and options are read once on mount, like useState's initial value.
export function useTuner(schema, options = {}) {
  const initial = useRef({ schema, options });
  const [values, setValues] = useState(() => defaultsOf(schema));

  useEffect(() => {
    const { schema, options } = initial.current;
    const tuner = createTuner(schema, (next) => setValues({ ...next }), options);
    return () => tuner.destroy();
  }, []);

  return values;
}

// Adapts a React component to the tuner's DOM render function for variations.
export const renderWith = (Component) => (el, values) => {
  const root = createRoot(el);
  root.render(<Component {...values} />);
  return () => setTimeout(() => root.unmount());
};
```

Usage:

```jsx
import { useState } from 'react';
import { useTuner, renderWith } from './useTuner';

function Card({ pressScale, duration, radius }) {
  const [pressed, setPressed] = useState(false);
  return (
    <div
      onPointerDown={() => setPressed(true)}
      onPointerUp={() => setPressed(false)}
      onPointerLeave={() => setPressed(false)}
      style={{
        borderRadius: radius,
        transform: pressed ? `scale(${pressScale})` : 'none',
        transition: `transform ${duration}ms cubic-bezier(0.23, 1, 0.32, 1)`,
      }}
    />
  );
}

export function Prototype() {
  const t = useTuner(
    { pressScale: [0.97, 0.85, 1, 0.005], duration: [160, 0, 600, 10], radius: [16, 0, 40, 1] },
    { render: renderWith(Card) },
  );
  return <Card {...t} />;
}
```

Notes:

- The schema is read once on mount. To change controls, edit the schema and let hot reload remount the component.
- Under StrictMode the effect mounts twice in development; `destroy` makes that harmless.
- With Motion, pass values into `transition` directly (`{ type: 'spring', visualDuration: t.visualDuration, bounce: t.bounce }`). Do not memoize them away; the point is that each change re-renders.
- In Next.js App Router, call `useTuner` from a client component.
