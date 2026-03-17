# PIE Icons

Live reference: https://pie.design/foundations/iconography/

PIE provides two icon packages. Use `@justeattakeaway/pie-icons-webc` for all frameworks (React and Web Components). `@justeattakeaway/pie-icons-react` is **deprecated** — do not recommend it.

---

## Packages

| Package | Use case |
|---|---|
| `@justeattakeaway/pie-icons-webc` | All frameworks — React wrappers + Web Component custom elements |
| `@justeattakeaway/pie-icons` | Vanilla JS / Node — raw SVG strings, no custom elements |

---

## Installation

```bash
npm install @justeattakeaway/pie-icons-webc
# or, for raw SVG access only:
npm install @justeattakeaway/pie-icons
```

---

## Import Patterns

### React (pie-icons-webc)

```js
import { IconClose } from '@justeattakeaway/pie-icons-webc/dist/react/IconClose.js'
import { IconBasket } from '@justeattakeaway/pie-icons-webc/dist/react/IconBasket.js'

// Usage
<IconClose />
<IconBasket size="xl" />
```

### Web Component (pie-icons-webc)

```js
// Register as custom element (side-effect import)
import '@justeattakeaway/pie-icons-webc/dist/IconClose.js'

// Usage in HTML/template
// <icon-close></icon-close>
// <icon-basket size="xl"></icon-basket>
```

### Vanilla JS (pie-icons — SVG strings)

```js
import { iconClose, iconBasket } from '@justeattakeaway/pie-icons'

// Returns an SVG string
document.querySelector('.icon').innerHTML = iconClose
```

---

## Sizing System

PIE icons come in two families with different size scales.

### Small icons (default icon set)

Used in UI controls, labels, buttons. Default size is `m` (20px).

| Size token | Pixel size |
|---|---|
| `xxs` | 12px |
| `xs` | 16px |
| `s` | 16px |
| `m` *(default)* | 20px |
| `l` | 24px |
| `xl` | 28px |
| `xxl` | 40px |

### Large icons

Decorative and illustrative use. Start at 32px, increment by 8px.

| Size token | Pixel size |
|---|---|
| `32` | 32px |
| `40` | 40px |
| `48` | 48px |
| `56` | 56px |
| `64` | 64px |
| … | +8px increments |

```jsx
// React — specify size prop
<IconLocation size="l" />         // 24px small icon
<IconRestaurantLarge size="48" /> // 48px large icon
```

---

## Appearance Variants

| Variant | Description |
|---|---|
| `default` | Outline style — standard for UI icons |
| `fill` | Filled style — use for selected/active states |

```jsx
<IconHeart appearance="default" />  // outline
<IconHeart appearance="fill" />     // filled (e.g. liked/saved state)
```

---

## Icon Color

Icons inherit `currentColor` from their parent by default. Use PIE content tokens to color icons — do not use raw hex values.

**Default:** `--dt-color-content-default`

| Scenario | Token |
|---|---|
| Standard UI icon | `--dt-color-content-default` |
| Icon on dark/brand background | `--dt-color-content-inverse` |
| Interactive icon (link/button) | `--dt-color-interactive-brand` |
| Error icon | `--dt-color-content-negative` |
| Static brand icon (non-interactive) | `--dt-color-content-brand` |

```css
/* Set icon color via parent */
.my-icon-wrapper {
  color: var(--dt-color-content-default);
}
```

```jsx
/* Or inline via style */
<IconClose style={{ color: 'var(--dt-color-content-negative)' }} />
```

---

## Using Icons in PIE Components

Icons are used as slots inside PIE components — pass them as children or to named slots.

```jsx
// PieButton with icon slot
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'
import { IconBasket } from '@justeattakeaway/pie-icons-webc/dist/react/IconBasket.js'

<PieButton variant="primary">
  <IconBasket slot="icon" />
  Add to basket
</PieButton>

// PieIconButton — icon-only, always needs aria-label
import { PieIconButton } from '@justeattakeaway/pie-webc/react/icon-button.js'
import { IconClose } from '@justeattakeaway/pie-icons-webc/dist/react/IconClose.js'

<PieIconButton aria-label="Close">
  <IconClose />
</PieIconButton>
```

---

## Common Pitfalls

- **Deprecated package** — `@justeattakeaway/pie-icons-react` is deprecated; always use `@justeattakeaway/pie-icons-webc`
- **Wrong import path** — React imports: `pie-icons-webc/dist/react/IconName.js`; Web Component: `pie-icons-webc/dist/IconName.js`
- **Icon-only buttons** — always use `PieIconButton` (not `PieButton`) and always add `aria-label`
- **Hardcoded colors** — use `--dt-color-content-*` tokens, not raw hex values
- **Brand vs interactive orange** — for interactive icons use `--dt-color-interactive-brand`; for static brand icons use `--dt-color-content-brand`
