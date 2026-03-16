# PIE Component Catalog

Full catalog of PIE Web Components. Import paths follow the pattern:
- Web Component: `import '@justeattakeaway/pie-webc/components/<name>.js'`
- React: `import { Pie<Name> } from '@justeattakeaway/pie-webc/react/<name>.js'`

Browse all: https://pie.design/components/

---

## Forms & Inputs

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Button | `<pie-button>` | `PieButton` | Primary action element. Variants: primary, primary-alternative, secondary, outline, ghost, destructive, destructive-ghost, inverse, outline-inverse, ghost-inverse. Sizes: xsmall–large. States include loading. | https://pie.design/components/button/ |
| Icon Button | `<pie-icon-button>` | `PieIconButton` | Button containing only an icon. Requires `aria-label`. Same variants as button. | https://pie.design/components/icon-button/ |
| Text Input | `<pie-text-input>` | `PieTextInput` | Single-line text field. Types: alphanumeric, numeric, password. Sizes: small/medium/large. Supports leading/trailing content slots, placeholder, read-only, disabled, error state. | https://pie.design/components/text-input/ |
| Textarea | `<pie-textarea>` | `PieTextarea` | Multi-line text input. Supports resize, character count. Use when input likely spans multiple lines. | https://pie.design/components/textarea/ |
| Checkbox | `<pie-checkbox>` | `PieCheckbox` | Standard checkbox. Supports indeterminate state. | https://pie.design/components/checkbox/ |
| Checkbox Group | `<pie-checkbox-group>` | `PieCheckboxGroup` | Groups related checkboxes with a shared label. | https://pie.design/components/checkbox-group/ |
| Radio Button | `<pie-radio-button>` | `PieRadioButton` | Single radio option. Use inside a radio group. | https://pie.design/components/radio-button/ |
| Radio Group | `<pie-radio-group>` | `PieRadioGroup` | Wraps radio buttons; manages selection state. | https://pie.design/components/radio-group/ |
| Switch | `<pie-switch>` | `PieSwitch` | Toggle switch for on/off states (e.g. settings). | https://pie.design/components/switch/ |
| Select | `<pie-select>` | `PieSelect` | Styled native select dropdown. | https://pie.design/components/select/ |
| Date Picker | `<pie-date-picker>` | `PieDatePicker` | Date selection input. | https://pie.design/components/date-picker/ |
| Numeric Stepper | `<pie-numeric-stepper>` | `PieNumericStepper` | Increment/decrement number input. | https://pie.design/components/numeric-stepper/ |
| Slider | `<pie-slider>` | `PieSlider` | Range input slider. | https://pie.design/components/slider/ |
| Uploader | `<pie-uploader>` | `PieUploader` | File upload input. | https://pie.design/components/uploader/ |
| Form Label | `<pie-form-label>` | `PieFormLabel` | Label for form fields with optional required indicator. | https://pie.design/components/form-label/ |
| Assistive Text | `<pie-assistive-text>` | `PieAssistiveText` | Helper/error text below form fields. Variants: default, success, error. | https://pie.design/components/assistive-text/ |

---

## Navigation

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Link | `<pie-link>` | `PieLink` | Styled anchor. Variants: default, high-visibility, inverse. | https://pie.design/components/link/ |
| Breadcrumb | `<pie-breadcrumb>` | `PieBreadcrumb` | Breadcrumb navigation trail. | https://pie.design/components/breadcrumb/ |
| Tabs | `<pie-tabs>` | `PieTabs` | Tabbed navigation/content panels. Requires child tab and panel components — see below. | https://pie.design/components/tabs/ |
| Tab (item) | `<pie-tab>` | `PieTab` | Individual tab button inside `PieTabs`. Import from `pie-webc/react/tab.js`. | https://pie.design/components/tabs/ |
| Tab Panel | `<pie-tab-panel>` | `PieTabPanel` | Content panel associated with a tab. Import from `pie-webc/react/tab-panel.js`. | https://pie.design/components/tabs/ |
| Accordion | `<pie-accordion>` | `PieAccordion` | Collapsible content sections. | https://pie.design/components/accordion/ |
| Pagination | `<pie-pagination>` | `PiePagination` | Page navigation control. | https://pie.design/components/pagination/ |
| Progress Stepper | `<pie-progress-stepper>` | `PieProgressStepper` | Multi-step progress indicator. | https://pie.design/components/progress-stepper/ |
| Segmented Controls | `<pie-segmented-controls>` | `PieSegmentedControls` | Mutually exclusive option selector (like radio but visual). | https://pie.design/components/segmented-controls/ |

**Tabs usage pattern (React):**
```jsx
import { PieTabs } from '@justeattakeaway/pie-webc/react/tabs.js'
import { PieTab } from '@justeattakeaway/pie-webc/react/tab.js'
import { PieTabPanel } from '@justeattakeaway/pie-webc/react/tab-panel.js'

<PieTabs>
  <PieTab slot="tabs">Overview</PieTab>
  <PieTab slot="tabs">Reviews</PieTab>
  <PieTab slot="tabs">Menu</PieTab>

  <PieTabPanel slot="panels">Overview content</PieTabPanel>
  <PieTabPanel slot="panels">Reviews content</PieTabPanel>
  <PieTabPanel slot="panels">Menu content</PieTabPanel>
</PieTabs>
```
All three components must be imported separately. Never mix `PieTabs` with bare `<pie-tab>` custom element tags in a React project.

---

## Feedback & Status

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Notification | `<pie-notification>` | `PieNotification` | Inline alert. Variants: info, success, warning, error. Can be dismissible. | https://pie.design/components/notification/ |
| Toast | `<pie-toast>` | `PieToast` | Ephemeral status message. Auto-dismisses. | https://pie.design/components/toast/ |
| Spinner | `<pie-spinner>` | `PieSpinner` | Loading indicator. Variants: brand, secondary, secondary-dark, inverse, inverse-light. Sizes: xsmall–xlarge (16px–48px). Use for 2–5s wait times; avoid multiple on same page. | https://pie.design/components/spinner/ |
| Skeleton | `<pie-skeleton>` | — | Loading placeholder for content areas. | https://pie.design/components/skeleton/ |
| Progress Bar | `<pie-progress-bar>` | `PieProgressBar` | Determinate progress indicator. | https://pie.design/components/progress-bar/ |
| Rating | `<pie-rating>` | `PieRating` | Star/score rating display or input. | https://pie.design/components/rating/ |
| Badge | `<pie-badge>` | `PieBadge` | Count/status indicator. Variants: default, subtle, outline, strong, inverse. | https://pie.design/components/badge/ |
| Tag | `<pie-tag>` | `PieTag` | Categorization label. | https://pie.design/components/tag/ |

---

## Overlays

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Modal | `<pie-modal>` | `PieModal` | Dialog overlay. Supports heading, footer actions, scrollable body. Uses `$rounded-d` (16px) radius. | https://pie.design/components/modal/ |
| Bottom Sheet | `<pie-bottom-sheet>` | `PieBottomSheet` | Sheet anchored to bottom of viewport. For mobile-primary flows. | https://pie.design/components/bottom-sheet/ |
| Side Sheet | `<pie-side-sheet>` | `PieSideSheet` | Sheet sliding in from the side. For secondary navigation or detail panels. | https://pie.design/components/side-sheet/ |
| Cookie Banner | `<pie-cookie-banner>` | `PieCookieBanner` | GDPR cookie consent overlay. | https://pie.design/components/cookie-banner/ |
| Tooltip | `<pie-tooltip>` | `PieTooltip` | Short contextual hint on hover/focus. | https://pie.design/components/tooltip/ |
| Popover | `<pie-popover>` | `PiePopover` | Richer contextual overlay (more content than tooltip). | https://pie.design/components/popover/ |

---

## Display & Layout

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Card | `<pie-card>` | `PieCard` | Content container. Variants: default, outline, inverse. Supports interactive (clickable) mode. Uses `$rounded-c` (12px) radius. | https://pie.design/components/card/ |
| Divider | `<pie-divider>` | `PieDivider` | Horizontal/vertical separator. | https://pie.design/components/divider/ |
| List Item | `<pie-list-item>` | `PieListItem` | Standard or interactive list row. | https://pie.design/components/list-item/ |
| Carousel Indicator | `<pie-carousel-indicator>` | `PieCarouselIndicator` | Dot indicators for carousels/sliders. | https://pie.design/components/carousel-indicator/ |
| Thumbnail | `<pie-thumbnail>` | `PieThumbnail` | Small image display with fallback. | https://pie.design/components/thumbnail/ |
| Avatar | `<pie-avatar>` | `PieAvatar` | User representation: image or initials fallback. | https://pie.design/components/avatar/ |
| Map Pin | `<pie-map-pin>` | `PieMapPin` | Location marker for map interfaces. | https://pie.design/components/map-pin/ |

---

## Interactive

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Chip | `<pie-chip>` | `PieChip` | Filter/selection chip. Supports selected state and leading icon. | https://pie.design/components/chip/ |
| Toggle Button Group | `<pie-toggle-button-group>` | `PieToggleButtonGroup` | Grouped toggle buttons for option selection. | https://pie.design/components/toggle-button-group/ |
| FAB | `<pie-fab>` | `PieFab` | Floating Action Button. Prominent primary action. One per screen. | https://pie.design/components/fab/ |
| Dropdown | `<pie-dropdown>` | `PieDropdown` | Custom dropdown menu (not a native select). | https://pie.design/components/dropdown/ |
| Show More | `<pie-show-more>` | `PieShowMore` | Progressive disclosure — expand/collapse long content. | https://pie.design/components/show-more/ |

---

## Data

| Component | Tag | React | Description | Docs |
|---|---|---|---|---|
| Data Table | `<pie-data-table>` | `PieDataTable` | Tabular data display. | https://pie.design/components/data-table/ |

---

## Icons Package (separate from pie-webc)

```bash
npm install @justeattakeaway/pie-icons-webc
# React icons
npm install @justeattakeaway/pie-icons-react
```

```js
// Web component icon
import '@justeattakeaway/pie-icons-webc/dist/pie-icon-close.js'
// <pie-icon-close></pie-icon-close>

// React icon
import { IconClose } from '@justeattakeaway/pie-icons-react'
// <IconClose />
```

Browse all icons: https://pie.design/foundations/iconography/

---

## Legacy Libraries (not pie-webc)

For older stacks:
- **Fozzie** — Vue 2 / Nuxt 2 component library
- **Snacks** — React component library (Takeaway.com legacy)
- **Skip PIE** — React components (SkipTheDishes legacy)

PIE Web Components (`@justeattakeaway/pie-webc`) is the recommended library for all new projects and frameworks: Next.js 14, React 18, Nuxt 3, Vue 3, and Vanilla JS.

---

## Finding a Component

If unsure whether a component exists, fetch the live list:
https://pie.design/components/
