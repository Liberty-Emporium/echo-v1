# SKILL: Next.js SaaS Template

> Production SaaS starter with auth, billing, dashboard, and settings.

## Quick Start
```bash
npx create-next-app@latest saas-app --typescript --tailwind --app --src-dir
cd saas-app
npm install next-auth @auth/prisma-adapter @prisma/client stripe
npm install class-variance-authority clsx tailwind-merge
```

## Project Structure
```
saas-app/
├── src/app/
│   ├── (auth)/login/page.tsx
│   ├── (dashboard)/dashboard/page.tsx
│   ├── (dashboard)/billing/page.tsx
│   ├── (dashboard)/settings/page.tsx
│   ├── api/auth/[...nextauth]/route.ts
│   └── api/billing/webhook/route.ts
├── src/components/ui/ (Button, Card, Input, Badge)
├── src/lib/auth.ts, stripe.ts, prisma.ts, utils.ts
└── prisma/schema.prisma
```

## Auth (NextAuth v5)
```ts
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import { PrismaAdapter } from "@auth/prisma-adapter"
import { prisma } from "./prisma"

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [Google],
  session: { strategy: "jwt" },
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.sub!
      return session
    },
  },
})
```

## Stripe Billing
```ts
import Stripe from "stripe"
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

// Checkout session
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  customer_email: email,
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${url}/billing?success=true`,
  cancel_url: `${url}/billing?canceled=true`,
})

// Webhook (critical!)
const event = stripe.webhooks.constructEvent(body, sig, webhookSecret)
switch (event.type) {
  case "checkout.session.completed": // Update user plan
  case "customer.subscription.updated": // Update subscription
  case "customer.subscription.deleted": // Downgrade to free
}
```

## Dashboard Layout
```tsx
import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

export default async function DashboardLayout({ children }) {
  const session = await auth()
  if (!session) redirect("/login")
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  )
}
```

## Env Vars
```env
DATABASE_URL=""
NEXTAUTH_URL=""
NEXTAUTH_SECRET="$(openssl rand -hex 32)"
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
STRIPE_SECRET_KEY=""
STRIPE_WEBHOOK_SECRET=""
STRIPE_PRICE_ID_PRO=""
```

## Deployment
```bash
npx prisma db push
npx vercel --prod
```
