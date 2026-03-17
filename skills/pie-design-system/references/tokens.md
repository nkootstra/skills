# PIE Design Tokens

Live reference: https://pie.design/foundations/design-tokens/

Design tokens are named values that represent the visual design decisions in PIE. Use them instead of hardcoded values in all cases.

## Token Architecture

```
Global tokens (primitives)        Alias tokens (semantic)
$color-orange-30 = #FF8000   →    $color-interactive-brand
$spacing-16 = 16px           →    $spacing-d
$radius-12 = 12px            →    $rounded-c
```

**Always prefer alias tokens** — they have semantic meaning and adapt to light/dark themes automatically.

## CSS Custom Property Syntax

Tokens are exposed as CSS custom properties with the `--dt-` prefix (design token):

```css
color: var(--dt-color-content-primary);
background-color: var(--dt-color-interactive-brand);
padding: var(--dt-spacing-d);               /* 16px */
border-radius: var(--dt-radius-rounded-c);  /* cards/popovers */
```

---

## Color Tokens

### Global Color Palette (primitives — use alias tokens in products)

PIE's color palette uses named palettes. These are primitive values; use alias tokens in component code.

| Palette | Key shades |
|---|---|
| **Orange** (brand) | `$color-orange-0` #FFF2E5 · `$color-orange-25` #FF9933 · `$color-orange-30` #FF8000 · `$color-orange` #F36805 |
| **Truffle** (neutrals) | `$color-truffle-5` #FDFDFB · `$color-truffle-10` #F6F3EF · `$color-truffle-30` #E7E2DA · `$color-truffle-55` #BEB7AC · `$color-truffle-70` #59564F · `$color-truffle-100` #1C1A17 |
| **Charcoal** (neutrals dark) | `$color-charcoal-30` #D7D9DA · `$color-charcoal-50` #8C999B · `$color-charcoal-70` #3C4C4F · `$color-charcoal-80` #242E30 |
| **Red** (error/destructive) | `$color-red-5` #FFD2D1 · `$color-red-30` #F85C59 · `$color-red` #CC0300 |
| **Green** (success) | `$color-green-5` #CEEED3 · `$color-green-30` #68CA77 · `$color-green` #2B7836 |
| **Yellow** (warning) | `$color-yellow-10` #FFF8D6 · `$color-yellow` #FFD600 · `$color-yellow-75` #A38900 |
| **Blue** (info) | `$color-blue-5` #E4E9FB · `$color-blue-30` #9EAEF0 · `$color-blue` #3147AD |
| **Aubergine** (brand support) | `$color-aubergine-10` #E3CFE3 · `$color-aubergine-70` #5B3D5B |
| **Berry** | `$color-berry-10` #FBDFE3 · `$color-berry-70` #98696F |
| **Cupcake** | `$color-cupcake-10` #E8F1F2 · `$color-cupcake-70` #6A787A |
| **Turmeric** | `$color-turmeric-10` #FCEAC0 · `$color-turmeric-40` #F6C243 |
| **Latte** | `$color-latte-10` #F4EAD7 · `$color-latte-70` #81735B |
| **Tomato** | `$color-tomato-5` #FFD3BF · `$color-tomato-50` #F75E28 |

Full palette: https://pie.design/foundations/colour/tokens/global/

---

### Alias Color Tokens (use these in component code)

#### Content (text)
| CSS Variable | Usage |
|---|---|
| `--dt-color-content-primary` | Default body text |
| `--dt-color-content-secondary` | Subdued/secondary text |
| `--dt-color-content-disabled` | Disabled state text |
| `--dt-color-content-inverse` | Text on dark/brand backgrounds (auto adjusts in dark theme) |
| `--dt-color-content-brand` | Brand-colored text |
| `--dt-color-content-positive` | Success state text |
| `--dt-color-content-negative` | Error state text |
| `--dt-color-content-warning` | Warning state text |
| `--dt-color-content-info` | Informational text |

#### Interactive (buttons, links, controls)
| CSS Variable | Usage |
|---|---|
| `--dt-color-interactive-brand` | Primary brand action background |
| `--dt-color-interactive-brand-hover` | Hover state for brand actions |
| `--dt-color-interactive-brand-active` | Active/pressed state |
| `--dt-color-interactive-secondary` | Secondary action background |
| `--dt-color-interactive-secondary-hover` | Hover for secondary |
| `--dt-color-interactive-tertiary` | Ghost/tertiary action |
| `--dt-color-interactive-disabled` | Disabled action background |
| `--dt-color-interactive-inverse` | Interactive on dark background |
| `--dt-color-interactive-inverse-hover` | Hover for inverse interactive |

#### Background
| CSS Variable | Usage |
|---|---|
| `--dt-color-background-default` | Page/card default background |
| `--dt-color-background-subtle` | Subtly differentiated surface |
| `--dt-color-background-strong` | Stronger emphasis surface |
| `--dt-color-background-inverse` | Dark/inverted background |
| `--dt-color-background-overlay` | Overlay/scrim (modal backdrop) |

#### Border
| CSS Variable | Usage |
|---|---|
| `--dt-color-border-default` | Default border/divider |
| `--dt-color-border-subtle` | Subtle border (lighter) |
| `--dt-color-border-strong` | Strong/emphasis border |
| `--dt-color-border-brand` | Brand-colored border |
| `--dt-color-border-positive` | Success state border |
| `--dt-color-border-negative` | Error state border |

Full alias color tokens: https://pie.design/foundations/colour/tokens/alias/

---

## Colour Usage Rules

### Brand Orange vs Product Orange

PIE uses two distinct oranges with different roles — mixing them is a common mistake:

| Orange | Token | Use for |
|---|---|---|
| **Product Orange** (`#FF8000`) | `--dt-color-interactive-brand` | Interactive elements: buttons, icons, links |
| **Brand Orange** (`#F36805`) | `--dt-color-content-brand` | Non-interactive: logos, nav bars, brand moments |

> **Rule:** If the user can click/tap it, use Product Orange (`--dt-color-interactive-brand`). For brand decoration that isn't interactive, use Brand Orange (`--dt-color-content-brand`).

### Content Token Suffixes

The `-inverse`, `-light`, and `-dark` suffixes on content tokens have precise meanings:

| Suffix | Behaviour | When to use |
|---|---|---|
| `-inverse` | Light in light theme, dark in dark theme (auto-adapts) | Text on dark/brand backgrounds in both themes |
| `-light` | **Always stays light** regardless of theme | Text that pairs with Product Orange, error red — must remain readable in dark mode |
| `-dark` | **Always stays dark** regardless of theme | Text that pairs with brand colours that stay light in dark mode |

Examples:
```css
/* Text on a dark/brand background — adapts to theme automatically */
color: var(--dt-color-content-inverse);

/* Text alongside error (red bg stays dark in dark mode) — must always be light */
color: var(--dt-color-content-light);

/* Text alongside brand decoration — must always be dark */
color: var(--dt-color-content-dark);
```

### Opacity vs Solid Tokens

PIE provides both opacity-based and solid variants of some tokens:

| Context | Use |
|---|---|
| Solid background (most cases) | **Opacity tokens** — they blend correctly with the background |
| Blur/frosted-glass / transparency backgrounds | **Solid tokens** — opacity tokens look wrong on blurred surfaces |

### Color Space

PIE's palette is defined in **HSLuv** (perceptually uniform HSL), ensuring WCAG 2.1 contrast compliance across the full palette. You do not need to compute contrast manually — use alias tokens and PIE's semantic pairings.

---

## Spacing Tokens

PIE uses an 8px/4px grid. Token names are letters; numeric global tokens are the underlying values.

### Alias Spacing Scale

| CSS Variable | Pixel Value | When to use |
|---|---|---|
| `--dt-spacing-none` | 0px | Explicitly no spacing |
| `--dt-spacing-a-small` | 2px | Micro gaps (e.g. icon/text nudges) |
| `--dt-spacing-a` | 4px | Tight spacing (e.g. icon padding) |
| `--dt-spacing-b` | 8px | Small gaps (e.g. between label and input) |
| `--dt-spacing-c` | 12px | Moderate gaps |
| `--dt-spacing-d` | 16px | Standard spacing (most common) |
| `--dt-spacing-e` | 24px | Comfortable spacing (sections within a card) |
| `--dt-spacing-f` | 32px | Substantial gaps (between cards) |
| `--dt-spacing-g` | 40px | Major spacing (section breaks) |
| `--dt-spacing-h` | 56px | Large section breaks |
| `--dt-spacing-i` | 64px | Significant breaks |
| `--dt-spacing-j` | 80px | Maximum spacing |

> **Note:** Token names map directly to `--dt-spacing-<letter>`. e.g. `$spacing-d` in Figma = `var(--dt-spacing-d)` in CSS.

Full spacing tokens: https://pie.design/foundations/spacing/tokens/alias/

---

## Border Radius Tokens

### Alias Radius Scale

| CSS Variable | Pixel | Used for |
|---|---|---|
| `--dt-radius-rounded-none` | 0px | Explicitly no rounding |
| `--dt-radius-rounded-a` | 4px | Small tags |
| `--dt-radius-rounded-b` | 8px | Data viz, tags, logos, toast |
| `--dt-radius-rounded-c` | 12px | Cards, popovers, notifications, nav bars, side drawers |
| `--dt-radius-rounded-d` | 16px | Modals and sheets |
| `--dt-radius-rounded-e` | ~9999px | Toggles, FABs, pill buttons — fully rounded |

Full radius tokens: https://pie.design/foundations/radius/tokens/alias/

---

## Elevation (Shadow) Tokens

| CSS Variable | Usage |
|---|---|
| `--dt-elevation-01` | Low elevation (subtle card shadow) |
| `--dt-elevation-02` | Medium elevation (dropdowns, tooltips) |
| `--dt-elevation-03` | High elevation (modals, overlays) |

---

## Blur Tokens

PIE provides blur (backdrop-filter) tokens for use in frosted-glass UI surfaces — e.g. nav bars, overlays, modals on photo backgrounds.

> **Android caveat:** `backdrop-filter` is not supported on Android WebView. Use blur tokens only for iOS/web; provide a solid fallback background for Android.

| CSS Variable | Usage |
|---|---|
| `--dt-blur-base` | Subtle blur — light overlay surfaces |
| `--dt-blur-neutral` | Moderate blur — nav bars, sticky headers |
| `--dt-blur-prominent` | Strong blur — modals, sheets on imagery |

### Container fill pairings

Blur alone looks wrong without a semi-transparent background. Pair blur tokens with the matching container fill token:

| Blur token | Container fill token | Use case |
|---|---|---|
| `--dt-blur-base` | `--dt-color-container-base` | Light surface on subtle bg |
| `--dt-blur-neutral` | `--dt-color-container-neutral` | Nav bar |
| `--dt-blur-prominent` | `--dt-color-container-prominent` | Modal on imagery |

```css
.frosted-nav {
  backdrop-filter: var(--dt-blur-neutral);
  background-color: var(--dt-color-container-neutral);
}
```

Full blur tokens: https://pie.design/foundations/blur/

---

## Typography

PIE's primary typeface is **JET Sans Digital** (variable font, weight 100–1000).
Fallback: Arial. Code snippets: PT Mono.

**Font loading:** `@justeattakeaway/pie-css` includes the JET Sans Digital font-face declarations. Import it at your app entry point — without it, browsers will fall back to Arial and the design will look wrong.

```js
import '@justeattakeaway/pie-css'  // loads JET Sans Digital + all --dt-* tokens
```

### Font families

| Family | Usage |
|---|---|
| JET Sans Digital | Primary — all product UI |
| Arial | Fallback only (loaded automatically if JET Sans Digital fails) |
| PT Mono | Code snippets only |

### Font weights

PIE uses 5 named weights (JET Sans Digital is a variable font):

| CSS Variable | Approx. Value | Usage |
|---|---|---|
| `--dt-font-weight-regular` | 400 | Body, captions, subheadings |
| `--dt-font-weight-bold` | 700 | Body strong, caption strong, interactive XS |
| `--dt-font-weight-extrabold` | 800 | Interactive L/S, subheading L (narrow), caption strong italic |
| `--dt-font-weight-black` | 900 | Headings XS–L |
| `--dt-font-weight-extrablack` | 950 | Headings XL–XXL |

### Alias typography tokens (use these — not raw size/weight tokens)

PIE exposes composite typography tokens that bundle font-size, line-height, weight, and family together. Prefer these over assembling raw tokens manually.

Token names in Figma map to CSS custom properties with the same name: `$font-heading-l` → `var(--dt-font-heading-l)`.

#### Headings (wide / narrow — responsive at 768px)

| Token | Wide size | Narrow size | Weight |
|---|---|---|---|
| `--dt-font-heading-xxl` | 48px / 52px lh | 32px / 36px lh | extra-black |
| `--dt-font-heading-xl` | 32px / 36px lh | 28px / 32px lh | extra-black |
| `--dt-font-heading-l` | 28px / 32px lh | 24px / 28px lh | black |
| `--dt-font-heading-m` | 24px / 28px lh | 20px / 24px lh | black |
| `--dt-font-heading-s` | 20px / 24px lh | 16px / 20px lh | black |
| `--dt-font-heading-xs` | 16px / 20px lh | 14px / 20px lh | black |

Italic variants: append `-italic` (e.g. `--dt-font-heading-l-italic`). Use for brand moments and speed/delivery messaging — not for UI controls.

#### Subheadings

| Token | Wide size | Narrow size | Weight |
|---|---|---|---|
| `--dt-font-subheading-l` | 24px / 28px lh | 20px / 24px lh | extra-bold |
| `--dt-font-subheading-s` | 20px / 24px lh | 16px / 24px lh | regular |

#### Body

| Token | Size | Line height | Weight | Notes |
|---|---|---|---|---|
| `--dt-font-body-l` | 16px | 24px | regular | Long-form reading |
| `--dt-font-body-l-link` | 16px | 24px | regular | Link in body text (underline) |
| `--dt-font-body-s` | 14px | 20px | regular | Components |
| `--dt-font-body-s-link` | 14px | 20px | regular | Link in small body (underline) |
| `--dt-font-body-strong-l` | 16px | 24px | bold | Emphasis in body |
| `--dt-font-body-strong-l-link` | 16px | 24px | bold | Bold link |
| `--dt-font-body-strong-s` | 14px | 20px | bold | Emphasis in small body |
| `--dt-font-body-strong-s-link` | 14px | 20px | bold | Bold small link |

#### Caption

| Token | Size | Line height | Weight |
|---|---|---|---|
| `--dt-font-caption` | 12px | 16px | regular |
| `--dt-font-caption-link` | 12px | 16px | regular (underline) |
| `--dt-font-caption-strong` | 12px | 16px | bold |
| `--dt-font-caption-strong-italic` | 12px | 16px | extra-bold + italic |
| `--dt-font-caption-strong-link` | 12px | 16px | bold (underline) |

#### Interactive (button labels)

| Token | Size | Line height | Weight | Usage |
|---|---|---|---|---|
| `--dt-font-interactive-l` | 20px | 24px | extra-bold | Large buttons, numeric counters |
| `--dt-font-interactive-s` | 16px | 20px | extra-bold | Small buttons |
| `--dt-font-interactive-xs` | 14px | 20px | bold | Extra-small buttons |

### Global font size tokens (raw — use alias tokens above instead)

| CSS Variable | Size |
|---|---|
| `--dt-font-size-12` | 12px |
| `--dt-font-size-14` | 14px |
| `--dt-font-size-16` | 16px |
| `--dt-font-size-20` | 20px |
| `--dt-font-size-24` | 24px |
| `--dt-font-size-28` | 28px |
| `--dt-font-size-32` | 32px |
| `--dt-font-size-48` | 48px |

### Typography Context

- **Responsive headings:** Heading and subheading tokens have `wide` and `narrow` variants. The breakpoint is **768px** — below 768px use the narrow variant values, above use wide.
- **Paragraph spacing:** 16px default (`--dt-spacing-d`), 14px for long-form text, 12px for tight exception cases.
- **Line length:** Keep text columns to **80–100 characters** for readability.


Full typography tokens: https://pie.design/foundations/typography/tokens/alias/wide/

---

## Motion Tokens

| CSS Variable | Usage |
|---|---|
| `--dt-motion-easing-default` | Standard transitions |
| `--dt-motion-easing-entrance` | Elements entering the DOM |
| `--dt-motion-easing-exit` | Elements leaving the DOM |
| `--dt-motion-duration-short-01` | Fast/micro animations |
| `--dt-motion-duration-moderate-01` | Standard UI transitions |
| `--dt-motion-duration-long-01` | Complex/large animations |

---

## Fetching the Latest Tokens

Token names evolve. Authoritative sources:
- Alias tokens: https://pie.design/foundations/design-tokens/
- Source: `@justeattakeaway/pie-css` (includes all CSS custom property definitions)
- GitHub: https://github.com/justeattakeaway/pie
