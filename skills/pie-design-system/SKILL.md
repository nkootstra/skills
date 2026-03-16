---
name: pie-design-system
description: "PIE design system expert for Just Eat Takeaway frontend developers. Use when working with PIE components, pie-webc, @justeattakeaway packages, pie.design, JET design system, design tokens, or implementing Figma designs with PIE. Covers component selection, correct import paths for Web Components and React wrappers, design token application, and framework setup (React, Next.js, Vue, Nuxt). NOT triggered for generic React/CSS questions unrelated to PIE."
---

# PIE Design System

PIE (Platform Ingredients for Everyone) is Just Eat Takeaway's design system. It provides 60+ production-ready components as Web Components (`@justeattakeaway/pie-webc`) with first-class React wrappers. This skill guides you to the right component, correct imports, proper token usage, and framework-specific setup — and cross-references Figma designs when needed.

## Step 1: Identify the Right Component

Map the user's UI need to a PIE component name. Use this quick reference:

| UI Need | PIE Component | Tag / React Name |
|---|---|---|
| Button / CTA | pie-button | `<pie-button>` / `PieButton` |
| Icon-only button (no label) | pie-icon-button | `<pie-icon-button>` / `PieIconButton` — always needs `aria-label` |
| Text input | pie-text-input | `<pie-text-input>` / `PieTextInput` |
| Textarea | pie-textarea | `<pie-textarea>` / `PieTextarea` |
| Checkbox (single) | pie-checkbox | `<pie-checkbox>` / `PieCheckbox` |
| Checkbox group (multiple) | pie-checkbox-group + pie-checkbox | `PieCheckboxGroup` wrapping `PieCheckbox` children — always use the group |
| Radio button | pie-radio-button | `<pie-radio-button>` / `PieRadioButton` |
| Toggle / Switch | pie-switch | `<pie-switch>` / `PieSwitch` — controlled via `checked` prop |
| Select / Dropdown | pie-select | `<pie-select>` / `PieSelect` |
| Form group | pie-form-label | `<pie-form-label>` / `PieFormLabel` |
| Form helper / error text | pie-assistive-text | `<pie-assistive-text>` / `PieAssistiveText` — use `variant="error"` for errors |
| Modal / Dialog | pie-modal | `<pie-modal>` / `PieModal` |
| Notification banner | pie-notification | `<pie-notification>` / `PieNotification` |
| Toast | pie-toast | `<pie-toast>` / `PieToast` |
| Loading indicator | pie-spinner | `<pie-spinner>` / `PieSpinner` |
| Skeleton loader | pie-skeleton | `<pie-skeleton>` (Web Component only — no React wrapper yet) |
| Link | pie-link | `<pie-link>` / `PieLink` |
| Chip / Tag | pie-chip | `<pie-chip>` / `PieChip` |
| Badge | pie-badge | `<pie-badge>` / `PieBadge` |
| Avatar | pie-avatar | `<pie-avatar>` / `PieAvatar` |
| Card (static) | pie-card | `<pie-card>` / `PieCard` |
| Card (clickable) | pie-card | `PieCard` with `interactive` prop — do NOT wrap in `<a>` |
| Divider | pie-divider | `<pie-divider>` / `PieDivider` |
| Accordion | pie-accordion | `<pie-accordion>` / `PieAccordion` |
| Tabs | pie-tabs | `PieTabs` + `PieTab` + `PieTabPanel` (three separate imports) |
| Side panel / filter drawer (desktop) | pie-side-sheet | `<pie-side-sheet>` / `PieSideSheet` — desktop only |
| Bottom panel (mobile) | pie-bottom-sheet | `<pie-bottom-sheet>` / `PieBottomSheet` — mobile only |
| Tooltip | pie-tooltip | `<pie-tooltip>` / `PieTooltip` |
| Popover | pie-popover | `<pie-popover>` / `PiePopover` |
| Cookie banner | pie-cookie-banner | `<pie-cookie-banner>` / `PieCookieBanner` |

For the full catalog with import paths and docs links, read `references/components.md`.

**Not sure which component to use?** When the user asks "what should I use for X" or when multiple components could fit (modal vs side sheet, notification vs toast, spinner vs skeleton, chip vs tag, etc.), read `references/component-selection.md` for decision guidance before answering.

## Step 2: Use the Correct Import

There are two patterns. Show the one that matches the user's framework.

**Web Components (any framework — registers `<pie-*>` custom elements):**
```js
import '@justeattakeaway/pie-webc/components/button.js'
// Then use: <pie-button variant="primary">Click me</pie-button>
```

**React wrapper (preferred for React/Next.js projects):**
```js
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'
// Then use: <PieButton variant="primary">Click me</PieButton>
```

React component naming: `Pie` prefix + PascalCase. Examples: `PieButton`, `PieTextInput`, `PieModal`, `PieCheckboxGroup`.

**Icons are a separate package — use the right one for the framework:**
```js
// React projects → pie-icons-react
import { IconClose, IconBasket } from '@justeattakeaway/pie-icons-react'
// npm install @justeattakeaway/pie-icons-react

// Web Component / non-React → pie-icons-webc
import '@justeattakeaway/pie-icons-webc/dist/pie-icon-close.js'
// npm install @justeattakeaway/pie-icons-webc
```

**Install the component package:**
```bash
npm install @justeattakeaway/pie-webc
```

## Step 3: Apply Design Tokens

**Never hardcode hex colors, spacing values, or border radius.** Use PIE design tokens.

Token architecture:
- **Global tokens** — primitive values, e.g. `$color-orange-30` = #FF8000
- **Alias tokens** — semantic meaning, e.g. `--dt-color-interactive-brand`. Always prefer these.

Key alias tokens:
```css
/* Colors */
color: var(--dt-color-content-primary);       /* body text */
color: var(--dt-color-content-inverse);       /* text on dark/brand backgrounds — NOT "inverted" */
background: var(--dt-color-interactive-brand);
border-color: var(--dt-color-border-negative); /* error state */

/* Spacing (a=4px, b=8px, c=12px, d=16px, e=24px, f=32px, g=40px) */
padding: var(--dt-spacing-d);   /* 16px */
gap: var(--dt-spacing-b);       /* 8px */

/* Radius */
border-radius: var(--dt-radius-rounded-c);   /* cards, popovers — 12px */
border-radius: var(--dt-radius-rounded-d);   /* modals, sheets — 16px */
```

Token prefix: `--dt-` (design token). The inverse text token is `--dt-color-content-inverse` (not "inverted").

For the full token catalog, read `references/tokens.md`.

## Step 4: Framework-Specific Setup

**Always include `@justeattakeaway/pie-css` in the app entry point.** Without it, design tokens (`--dt-*`) won't resolve and components will render unstyled.

```js
// src/main.jsx / src/index.js / app/layout.tsx
import '@justeattakeaway/pie-css'
```

Different frameworks need additional configuration. Read `references/framework-guides.md` for:
- **React** (CRA / Vite) — no special config beyond the `pie-css` import above
- **Next.js 14 (App Router)** — also needs `transpilePackages: ['@justeattakeaway/pie-webc']` in `next.config.js`
- **Nuxt 3** — needs `transpile` and `moduleSideEffects` config
- **Vue 3** — needs `isCustomElement: (tag) => tag.startsWith('pie-')` in Vite config

## Step 5: Cross-Reference Figma

Use the Figma MCP in two situations:

### 5a. Implementing a specific design
When the user provides a Figma URL:
1. Extract `fileKey` and `nodeId` from the URL (file key = segment after `/design/`)
2. Call `get_design_context` with those values
3. Map the returned design to the appropriate PIE component using the catalog

URL format: `figma.com/design/<fileKey>/<fileName>?node-id=<nodeId>`
Convert node-id dash separator to colon: `123-456` → `123:456`

### 5b. Checking component usage guidelines
When baked-in guidance in `references/component-selection.md` is insufficient:
1. Ask the user to share the PIE Figma URL or use the file they have access to
2. Call `get_metadata` on the file to discover pages
3. Call `get_design_context` on the relevant component node for do/don't annotations

## Step 6: Fetch Live Docs When Needed

This skill's baked-in knowledge may be out of date. If uncertain about props, variant names, or whether a component exists:

```
Component docs:  https://pie.design/components/<component-name>/
Token reference: https://pie.design/foundations/design-tokens/
Full component list: https://pie.design/components/
```

Always prefer live docs over baked-in knowledge for prop details.

## Step 7: Output Format

Every response must include:

1. **Why this component** — one sentence explaining why this component is the right choice (e.g. "PieAssistiveText is the dedicated component for form field helper and error text — do not use the `supportingText` prop")
2. **Component name** — Web Component tag and React name
3. **Install** — `npm install @justeattakeaway/pie-webc` + `@justeattakeaway/pie-css` (if not already set up)
4. **Import** — the framework-appropriate import (React wrapper or Web Component)
5. **Usage snippet** — minimal, working example with correct prop names
6. **Relevant tokens** — any `--dt-*` tokens the developer should use in surrounding layout
7. **Docs link** — `https://pie.design/components/<name>/`

Example output for "Add a primary button":
```jsx
// React
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'

<PieButton variant="primary" type="submit">
  Place Order
</PieButton>
```
Docs: https://pie.design/components/button/

## Common Pitfalls

**Component selection:**
- **Icon-only button** — use `PieIconButton` (not `PieButton`); always add `aria-label`
- **Checkbox group** — always wrap `PieCheckbox` components in `PieCheckboxGroup`; never group them manually with a `<div>`
- **Clickable card** — use `PieCard` with the `interactive` prop; never wrap a card in an `<a>` tag
- **Desktop side panel / filter drawer** — use `PieSideSheet`; `PieBottomSheet` is mobile-only and wrong for desktop
- **Form error text** — use `PieAssistiveText` with `variant="error"`; there is no `supportingText` prop on `PieTextInput`

**Prop names:**
- Button destructive variant is `variant="destructive"` — not `"danger"`
- Text on dark/brand backgrounds: `--dt-color-content-inverse` — not `"inverted"`
- PieSwitch controlled state uses `checked` prop (not `isChecked`) and `onChange` handler
- Error notifications (`variant="error"`) **never auto-dismiss** — always persist until the user acts

**Setup:**
- **Missing `@justeattakeaway/pie-css`** — must be imported in the app entry point or tokens won't resolve
- **Wrong icon package in React** — use `@justeattakeaway/pie-icons-react`; `pie-icons-webc` is for non-React projects
- **Wrong import path** — React wrappers: `pie-webc/react/<name>.js`; Web Components: `pie-webc/components/<name>.js`
- **Missing side-effect import** — Web Components need `import '@justeattakeaway/pie-webc/components/foo.js'` or the tag renders as a plain `HTMLElement`
- **Next.js App Router** — add `transpilePackages: ['@justeattakeaway/pie-webc']` and mark files with event handlers as `'use client'`

**Uncertainty:**
- If unsure whether a component or prop exists, fetch live docs at `https://pie.design/components/<name>/` before answering
