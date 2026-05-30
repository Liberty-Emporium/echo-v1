# SKILL: Tailwind CSS Design System

> Rapid UI development with Tailwind CSS, design tokens, and component architecture.

## Core Concepts

### Utility-First Philosophy
```html
<div class="bg-white rounded-lg shadow-md p-6 max-w-sm">
  <h2 class="text-xl font-semibold text-gray-800 mb-4">Heading</h2>
</div>
```

### Design Tokens (tailwind.config.js)
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: { 500: '#3b82f6', 700: '#1d4ed8', 900: '#1e3a5f' }
      }
    }
  }
}
```

### Component Pattern (with CVA)
```tsx
import { cva } from 'class-variance-authority'

const buttonVariants = cva("inline-flex items-center rounded-md font-medium", {
  variants: {
    variant: {
      default: "bg-blue-500 text-white hover:bg-blue-700",
      outline: "border border-gray-300 hover:bg-gray-50",
    },
    size: {
      default: "h-10 px-4 py-2",
      sm: "h-8 px-3 text-sm",
    },
  },
  defaultVariants: { variant: "default", size: "default" },
})
```

### shadcn/ui Pattern (Recommended)
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card dialog form input
```

### Dark Mode
```html
<html class="dark">
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

### Responsive Design
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

## Pitfalls
1. Long utility strings → extract to components
2. Not using design tokens → always define custom config
3. Ignoring mobile-first → sm: → md: → lg: → xl:
