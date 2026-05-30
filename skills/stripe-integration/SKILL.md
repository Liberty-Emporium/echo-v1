# SKILL: Stripe Integration

> Subscriptions, one-time payments, webhooks, customer portal.

## Setup
```bash
npm install stripe @stripe/stripe-js
# Python: pip install stripe
```

## Plans
```typescript
export const PLANS = {
  free: { name: "Free", price: 0 },
  pro: { name: "Pro", price: 2900, priceId: process.env.STRIPE_PRICE_ID_PRO },
  enterprise: { name: "Enterprise", price: 9900, priceId: process.env.STRIPE_PRICE_ID_ENT },
}
```

## Checkout Session
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  customer_email: user.email,
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${url}/billing?success=true`,
  cancel_url: `${url}/billing?canceled=true`,
  subscription_data: { metadata: { userId: user.id } },
})
return { url: session.url }
```

## Webhook (Critical!)
```typescript
const event = stripe.webhooks.constructEvent(body, sig, webhookSecret)

switch (event.type) {
  case "checkout.session.completed":
    // Create/update user plan
    break
  case "customer.subscription.updated":
    // Update subscription status
    break
  case "customer.subscription.deleted":
    // Downgrade to free
    break
  case "invoice.payment_failed":
    // Notify user
    break
}
return { status: "ok" }
```

## Customer Portal
```typescript
const portal = await stripe.billingPortal.sessions.create({
  customer: user.stripeCustomerId,
  return_url: `${url}/billing`,
})
return { url: portal.url }
```

## Python (FastAPI)
```python
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

@app.post("/api/billing/checkout")
async def checkout(price_id: str, user=Depends(get_current_user)):
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer_email=user.email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{FRONTEND_URL}/billing?success=true",
        cancel_url=f"{FRONTEND_URL}/billing?canceled=true",
    )
    return {"url": session.url}

@app.post("/api/billing/webhook")
async def webhook(request: Request):
    event = stripe.Webhook.construct_event(
        await request.body(),
        request.headers["stripe-signature"],
        settings.STRIPE_WEBHOOK_SECRET,
    )
    # Handle event types...
    return {"status": "ok"}
```

## Security
1. Always verify webhook signature
2. Make webhooks idempotent (check event ID)
3. Respond 200 quickly, process async
4. Test with Stripe CLI: `stripe listen --forward-to localhost:3000/api/webhooks`
