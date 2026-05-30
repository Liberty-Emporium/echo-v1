# SKILL: Tailwind Component Library

> Liberty Emporium design system — reusable UI components.

## Design Tokens
```js
// tailwind.config.ts
colors: {
  brand: { 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8", 900: "#1e3a8a" }
}
```

## Button
```tsx
import { cva } from "class-variance-authority"
const buttonVariants = cva("inline-flex items-center rounded-lg font-medium transition-colors", {
  variants: {
    variant: {
      default: "bg-brand-500 text-white hover:bg-brand-600",
      secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 dark:bg-gray-800 dark:text-white",
      outline: "border-2 border-brand-500 text-brand-500 hover:bg-brand-50",
      ghost: "hover:bg-gray-100 dark:hover:bg-gray-800",
      danger: "bg-red-500 text-white hover:bg-red-600",
    },
    size: {
      sm: "h-9 px-3 text-sm",
      default: "h-11 px-5 text-sm",
      lg: "h-14 px-6 text-base",
      icon: "h-10 w-10",
    },
  },
  defaultVariants: { variant: "default", size: "default" },
})
```

## Card
```tsx
export function Card({ className, ...props }) {
  return <div className={cn("bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700", className)} {...props} />
}
export function CardTitle({ className, ...props }) {
  return <h3 className={cn("text-lg font-semibold text-gray-900 dark:text-white", className)} {...props} />
}
export function CardContent({ className, ...props }) {
  return <div className={cn("p-6", className)} {...props} />
}
```

## Input
```tsx
export const Input = forwardRef<HTMLInputElement, InputProps>(({ label, error, hint, className, ...props }, ref) => (
  <div className="space-y-1.5">
    {label && <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">{label}</label>}
    <input ref={ref} className={cn("w-full h-11 px-4 rounded-lg border bg-white dark:bg-gray-800 focus:ring-2 focus:ring-brand-500", error ? "border-red-500" : "border-gray-300 dark:border-gray-600", className)} {...props} />
    {hint && !error && <p className="text-xs text-gray-500">{hint}</p>}
    {error && <p className="text-xs text-red-500">{error}</p>}
  </div>
))
```

## Badge
```tsx
const badgeVariants = cva("inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium", {
  variants: {
    variant: {
      default: "bg-brand-100 text-brand-800 dark:bg-brand-900 dark:text-brand-200",
      success: "bg-green-100 text-green-800",
      warning: "bg-yellow-100 text-yellow-800",
      danger: "bg-red-100 text-red-800",
    },
  },
})
```

## Navbar
```tsx
export function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link href="/" className="text-xl font-bold text-brand-500">Brand</Link>
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm">Log in</Button>
          <Button size="sm">Get Started</Button>
        </div>
      </div>
    </nav>
  )
}
```

## Utility
```ts
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs) { return twMerge(clsx(inputs)) }
```
