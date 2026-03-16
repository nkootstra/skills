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
| Text input | pie-text-input | `<pie-text-input>` / `PieTextInput` |
| Textarea | pie-textarea | `<pie-textarea>` / `PieTextarea` |
| Checkbox | pie-checkbox | `<pie-checkbox>` / `PieCheckbox` |
| Radio button | pie-radio-button | `<pie-radio-button>` / `PieRadioButton` |
| Toggle / Switch | pie-switch | `<pie-switch>` / `PieSwitch` |
| Select / Dropdown | pie-select | `<pie-select>` / `PieSelect` |
| Form group | pie-form-label | `<pie-form-label>` / `PieFormLabel` |
| Modal / Dialog | pie-modal | `<pie-modal>` / `PieModal` |
| Notification / Toast | pie-notification | `<pie-notification>` / `PieNotification` |
| Loading indicator | pie-spinner | `<pie-spinner>` / `PieSpinner` |
| Skeleton loader | pie-skeleton | Not yet in React wrappers |
| Link | pie-link | `<pie-link>` / `PieLink` |
| Icon | pie-icon | `<pie-icon>` / `PieIcon` |
| Chip / Tag | pie-chip | `<pie-chip>` / `PieChip` |
| Badge | pie-badge | `<pie-badge>` / `PieBadge` |
| Avatar | pie-avatar | `<pie-avatar>` / `PieAvatar` |
| Card | pie-card | `<pie-card>` / `PieCard` |
| Divider | pie-divider | `<pie-divider>` / `PieDivider` |
| Assistive text | pie-assistive-text | `<pie-assistive-text>` / `PieAssistiveText` |
| Cookie banner | pie-cookie-banner | `<pie-cookie-banner>` / `PieCookieBanner` |
| Accordion | pie-accordion | `<pie-accordion>` / `PieAccordion` |
| Tabs | pie-tabs | `<pie-tabs>` / `PieTabs` |
| Bottom Sheet | pie-bottom-sheet | `<pie-bottom-sheet>` / `PieBottomSheet` |
| Tooltip | pie-tooltip | `<pie-tooltip>` / `PieTooltip` |
| Popover | pie-popover | `<pie-popover>` / `PiePopover` |
| Rating | pie-rating | `<pie-rating>` / `PieRating` |

For the full catalog with import paths and docs links, read `references/components.md`.

**Not sure which component to use?** When the user asks "what should I use for X" or when multiple components could fit (modal vs bottom sheet, notification vs toast, spinner vs skeleton, chip vs tag, etc.), read `references/component-selection.md` for decision guidance before answering.

## Step 2: Use the Correct Import

There are two patterns. Always show **both** and indicate which to use.

**Web Components (works in any framework — registers `<pie-*>` custom elements):**
```js
import '@justeattakeaway/pie-webc/components/button.js'
// Then use: <pie-button variant="primary">Click me</pie-button>
```

**React wrapper (preferred for React/Next.js projects):**
```js
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'
// Then use: <PieButton variant="primary">Click me</PieButton>
```

React component naming: `Pie` prefix + PascalCase component name. Examples:
- `PieButton`, `PieTextInput`, `PieModal`, `PieSpinner`, `PieCheckbox`

The React wrappers are thin wrappers around the Web Components — same props/API, just typed React components.

**Install the package:**
```bash
npm install @justeattakeaway/pie-webc
# or
yarn add @justeattakeaway/pie-webc
```

## Step 3: Apply Design Tokens

**Never hardcode hex colors, spacing values, or border radius.** Use PIE design tokens.

Token architecture:
- **Global tokens** — primitive values: `$color-orange-30`, `$spacing-d`, `$radius-rounded-b`
- **Alias tokens** — semantic meaning: `$color-interactive-brand`, `$color-content-primary`, `$spacing-form-field`

Use alias tokens wherever possible. They adapt to light/dark themes automatically.

Common token examples:
```css
/* Colors */
color: var(--dt-color-content-primary);
background: var(--dt-color-interactive-brand);
border-color: var(--dt-color-border-default);

/* Spacing (a=4px, b=8px, c=12px, d=16px, e=24px, f=32px, g=40px) */
padding: var(--dt-spacing-d);   /* 16px */
gap: var(--dt-spacing-b);       /* 8px */

/* Radius */
border-radius: var(--dt-radius-rounded-c);   /* cards, popovers */
border-radius: var(--dt-radius-rounded-d);   /* modals, sheets */
border-radius: var(--dt-radius-rounded-e);   /* pill / fully rounded */
```

Token CSS custom property prefix: `--dt-` (design token).

For the full token catalog organized by category, read `references/tokens.md`.

## Step 4: Framework-Specific Setup

Different frameworks need different configuration. Read `references/framework-guides.md` for complete setup snippets covering:

- **React** (CRA / Vite) — straightforward, no special config
- **Next.js 14 (App Router)** — requires `moduleSideEffects` in Next config for web component registration
- **Nuxt 3** — requires `moduleSideEffects` in Nuxt config
- **Vue** — requires custom element registration or Fozzie integration

Key Next.js gotcha: Web Components need their side-effect imports bundled. Add to `next.config.js`:
```js
experimental: {
  optimizePackageImports: ['@justeattakeaway/pie-webc']
}
```

Or configure `transpilePackages` — see `references/framework-guides.md` for the full pattern.

## Step 5: Cross-Reference Figma

Use the Figma MCP in two situations:

### 5a. Implementing a specific design
When the user provides a Figma URL:
1. Extract `fileKey` and `nodeId` from the URL (file key = segment after `/design/`)
2. Call `get_design_context` with those values
3. Map the returned design to the appropriate PIE component using the catalog

URL format: `figma.com/design/<fileKey>/<fileName>?node-id=<nodeId>`
Convert node-id dash separator to colon: `123-456` → `123:456`

### 5b. Checking component usage guidelines in the PIE Figma library
When the user asks "which component should I use for X" and the baked-in guidance in `references/component-selection.md` is insufficient, check the PIE Figma file for richer "when to use" documentation:

1. Ask the user to share the URL to the relevant component page in the PIE Figma library, or use the PIE Core Web Components file if you already have access
2. Call `get_metadata` on the file to discover available pages — look for pages named "Components", "When to use", "Usage guidelines", or similar
3. Call `get_design_context` on the relevant component node to see usage annotations, do/don't examples, and variant guidance embedded in the design
4. Use any "do / don't" frames and annotation text from the design to supplement the guidance in `references/component-selection.md`

If the user hasn't provided a Figma URL, ask them to share it or direct them to `pie.design/components/<name>/` for the live docs.

## Step 6: Fetch Live Docs When Needed

This skill's baked-in knowledge may be out of date. If uncertain about:
- A component's available props or variant values
- Whether a component exists or has been renamed
- Exact token names

Fetch the live documentation:
```
Component docs:  https://pie.design/components/<component-name>/
Token reference: https://pie.design/foundations/design-tokens/
Full component list: https://pie.design/components/
```

Always prefer live docs over baked-in knowledge for prop details and API changes.

## Step 7: Output Format

Every response should include:

1. **Component name** — with Web Component tag and React name
2. **Install** — `npm install @justeattakeaway/pie-webc` (if not already installed)
3. **Import** — both Web Component and React import (or just the relevant one)
4. **Usage snippet** — minimal, working example
5. **Relevant tokens** — any token names the developer should use
6. **Docs link** — `https://pie.design/components/<name>/`

Example output for "Add a primary button":
```jsx
// React
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'

<PieButton variant="primary" type="submit">
  Place Order
</PieButton>
```
```js
// Web Component
import '@justeattakeaway/pie-webc/components/button.js'
// <pie-button variant="primary" type="submit">Place Order</pie-button>
```
Docs: https://pie.design/components/button/

## Common Pitfalls

- **Hardcoding hex values** — always use `--dt-color-*` tokens instead
- **Wrong import path** — it's `pie-webc/components/button.js` not `pie-webc/button`
- **Missing side-effect import** — Web Components need `import '@justeattakeaway/pie-webc/components/foo.js'` to register the custom element; forgetting this means the tag renders as `HTMLElement`
- **Using deprecated APIs** — fetch live docs at `https://pie.design/components/<name>/` for current props
- **React wrapper vs Web Component confusion** — React wrappers are under `pie-webc/react/<name>.js`; Web Components are under `pie-webc/components/<name>.js`
- **Icon imports** — icons come from a separate package: `@justeattakeaway/pie-icons-webc`
