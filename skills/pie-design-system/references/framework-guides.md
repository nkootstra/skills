# PIE Framework Integration Guides

Setup and integration patterns for each supported framework.

Live integration guides: https://pie.design/engineers/getting-started/

## Which library to use?

| Stack | Library |
|---|---|
| **Next.js 14 / React 18 / Nuxt 3 / Vue 3 / Vanilla JS** | `@justeattakeaway/pie-webc` ← recommended |
| Next.js 13 (no SSR needed) | `@justeattakeaway/pie-webc` |
| Next.js 13 (SSR needed) | Snacks (or upgrade to Next 14) |
| Vue 2 / Nuxt 2 | Fozzie |

---

## React (CRA / Vite)

No special configuration needed. Import the React wrapper and use it.

### Setup

```bash
npm install @justeattakeaway/pie-webc
```

### Usage

```jsx
// Import the React wrapper
import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'
import { PieTextInput } from '@justeattakeaway/pie-webc/react/text-input.js'

export function LoginForm() {
  return (
    <form>
      <PieTextInput
        name="email"
        type="email"
        placeholder="Enter your email"
      />
      <PieButton type="submit" variant="primary">
        Sign in
      </PieButton>
    </form>
  )
}
```

### Tokens in React

Import the PIE CSS variables in your app entry point:

```js
// src/index.js or src/main.jsx
import '@justeattakeaway/pie-css'
```

Or reference them in your global CSS:
```css
@import '@justeattakeaway/pie-css';
```

---

## Next.js 14 (App Router)

Web Components rely on side-effect imports for custom element registration. Next.js needs special configuration to bundle these correctly.

### Setup

```bash
npm install @justeattakeaway/pie-webc @justeattakeaway/pie-css
```

### next.config.js

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@justeattakeaway/pie-webc'],
  experimental: {
    optimizePackageImports: ['@justeattakeaway/pie-webc'],
  },
}

module.exports = nextConfig
```

### Global styles (app/layout.tsx)

```tsx
import '@justeattakeaway/pie-css'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Using React wrappers in App Router

React wrappers work in Server Components and Client Components. For components that use interactivity (event handlers), mark the file with `'use client'`:

```tsx
'use client'

import { PieButton } from '@justeattakeaway/pie-webc/react/button.js'

export function SubmitButton() {
  return (
    <PieButton variant="primary" type="submit">
      Place Order
    </PieButton>
  )
}
```

### Using Web Components in Next.js

If using bare Web Component tags (not React wrappers), ensure side-effect imports are in a client component:

```tsx
'use client'

import '@justeattakeaway/pie-webc/components/button.js'

export function PieButtonClient() {
  return <pie-button variant="primary">Click</pie-button>
}
```

---

## Nuxt 3

Nuxt requires similar module side-effects configuration to correctly bundle PIE's Web Component registrations.

### Setup

```bash
npm install @justeattakeaway/pie-webc @justeattakeaway/pie-css
```

### nuxt.config.ts

```ts
export default defineNuxtConfig({
  build: {
    transpile: ['@justeattakeaway/pie-webc'],
  },
  vite: {
    optimizeDeps: {
      include: ['@justeattakeaway/pie-webc'],
    },
    build: {
      rollupOptions: {
        // Ensure side-effect imports are preserved
        treeshake: {
          moduleSideEffects: (id) => id.includes('@justeattakeaway/pie-webc'),
        },
      },
    },
  },
})
```

### Global styles (app.vue or plugins)

```vue
<!-- app.vue -->
<script setup>
import '@justeattakeaway/pie-css'
</script>
```

Or as a Nuxt plugin:
```ts
// plugins/pie.ts
import '@justeattakeaway/pie-css'
export default defineNuxtPlugin(() => {})
```

### Using PIE in Vue components

```vue
<script setup lang="ts">
import '@justeattakeaway/pie-webc/components/button.js'
import '@justeattakeaway/pie-webc/components/text-input.js'
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <pie-text-input name="email" type="email" />
    <pie-button type="submit" variant="primary">Submit</pie-button>
  </form>
</template>
```

### Suppress custom element warnings in Nuxt/Vue

Add to your Nuxt config to prevent Vue from warning about unknown `pie-*` elements:

```ts
export default defineNuxtConfig({
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag.startsWith('pie-'),
    },
  },
})
```

---

## Vue 3 (standalone)

### Setup

```bash
npm install @justeattakeaway/pie-webc @justeattakeaway/pie-css
```

### vite.config.ts

```ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // Treat all pie-* tags as custom elements
          isCustomElement: (tag) => tag.startsWith('pie-'),
        },
      },
    }),
  ],
})
```

### main.ts

```ts
import { createApp } from 'vue'
import '@justeattakeaway/pie-css'
import App from './App.vue'

createApp(App).mount('#app')
```

### Component usage

```vue
<script setup lang="ts">
import '@justeattakeaway/pie-webc/components/button.js'
import '@justeattakeaway/pie-webc/components/spinner.js'
</script>

<template>
  <div>
    <pie-spinner v-if="loading" />
    <pie-button v-else variant="primary" @click="handleClick">
      Load Data
    </pie-button>
  </div>
</template>
```

---

## TypeScript Support

PIE Web Components ship with TypeScript definitions. For React wrappers, types are included automatically. For bare Web Component tags in TypeScript, extend the JSX/DOM types:

```ts
// pie-types.d.ts
import type { PieButtonProps } from '@justeattakeaway/pie-webc/components/button.js'

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'pie-button': PieButtonProps & React.HTMLAttributes<HTMLElement>
    }
  }
}
```

---

## Fozzie (JET Internal Build Tools)

If your project uses Fozzie (JET's internal webpack configuration), PIE components may already be configured. Check your `fozzie.config.js` for existing PIE setup before adding manual configuration.

---

## Troubleshooting

**Custom element not defined (renders as `<HTMLElement>`)**
- Ensure the side-effect import is executed: `import '@justeattakeaway/pie-webc/components/<name>.js'`
- In SSR environments, this import must run in a client context

**Styles not applied**
- Import `@justeattakeaway/pie-css` in your app root
- Check that CSS custom properties (`--dt-color-*`, etc.) are loaded globally

**TypeScript errors on custom element attributes**
- Add global type declarations as shown above, or use the React wrappers which include full TypeScript support

**Next.js build fails with Web Components**
- Add `@justeattakeaway/pie-webc` to `transpilePackages` in `next.config.js`
