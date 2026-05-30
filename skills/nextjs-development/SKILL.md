# SKILL: Next.js Development

> Production-grade Next.js development with App Router, Server Components, and modern patterns.

## When to Use
- Building full-stack React applications
- Need SSR/SSG/ISR rendering
- API + frontend in one project
- SEO-critical pages
- Vercel deployment

## Core Concepts

### App Router (`app/` directory)
```
app/
  layout.tsx        — Shared layout
  page.tsx          — Route page
  loading.tsx       — Loading state
  error.tsx         — Error boundary
  not-found.tsx     — 404 page
  api/              — API routes
    route.ts        — Edge/Node endpoint
```

### Server vs Client Components
```tsx
// Server Component (default) — no 'use client'
async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Client Component — needs interactivity
'use client';
import { useState } from 'react';
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Data Fetching
```tsx
// Server Component — direct async fetch
async function Page() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store', // dynamic
    // or { next: { revalidate: 3600 } } // ISR
  });
  const data = await res.json();
  return <List data={data} />;
}
```

### Server Actions (mutations)
```tsx
// app/actions.ts
'use server';
import { revalidatePath } from 'next/cache';

export async function createItem(formData: FormData) {
  const name = formData.get('name') as string;
  await db.items.create({ name });
  revalidatePath('/items');
}

// app/new/page.tsx
import { createItem } from './actions';
export default function NewPage() {
  return (
    <form action={createItem}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Route Handlers (API routes)
```ts
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const items = await db.items.findMany();
  return NextResponse.json(items);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const item = await db.items.create(body);
  return NextResponse.json(item, { status: 201 });
}
```

## Patterns & Best Practices

### Project Structure
```
src/
  app/              — Routes, pages, layouts
  components/       — Reusable UI
    ui/             — Base components (Button, Input, etc.)
    forms/          — Form components
    layout/         — Layout components
    sections/       — Page sections
  lib/              — Utility functions, config
  hooks/            — Custom hooks
  types/            — TypeScript types
  styles/           — Global styles
  server/           — Server-only code (DB, auth, etc.)
```

### Authentication
- **NextAuth.js (Auth.js v5)** — Universal (OAuth, credentials, magic links)
- **Clerk** — Managed auth, great DX
- **Supabase Auth** — If using Supabase
- **Better Auth** — Modern open-source option

### Styling
- **Tailwind CSS** — Primary recommendation
- **shadcn/ui** — Component library template (copy, don't install)
- **CSS Modules** — When Tailwind isn't enough

### Deployment (Vercel)
```bash
npx vercel              # Deploy
npx vercel --prod       # Production
npx vercel env pull     # Pull env vars
```

## Common Pitfalls
1. **Client/Server boundary** — can't pass functions as props to Server Components
2. **Waterfall fetches** — fetch in parallel with `Promise.all`
3. **Overusing 'use client'** — default to Server Components
4. **Environment variables** — `NEXT_PUBLIC_` prefix for client-accessible vars

## Performance Checklist
- [ ] Server Components by default
- [ ] `next/image` for images (automatic optimization)
- [ ] `next/font` for fonts (self-hosted, no layout shift)
- [ ] Dynamic imports for heavy client components
- [ ] Streaming with Suspense boundaries
- [ ] Metadata API for SEO
- [ ] Parallel routes where applicable
