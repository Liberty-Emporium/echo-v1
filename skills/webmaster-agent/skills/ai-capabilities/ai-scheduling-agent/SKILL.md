---
name: ai-scheduling-agent
description: AI-powered appointment scheduling and booking for small businesses — self-hosted Cal.com, automated reminders, calendar integration
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Scheduling Agent for Small Business

## When to use
- Adding online booking to a small business website
- Eliminating back-and-forth emails for appointments
- Automating appointment reminders
- Converting website visitors into scheduled appointments

## Key Stat
Autonomous booking systems eliminate the window between inquiry and confirmation, converting intent into scheduled revenue regardless of clock time (2026).

## Free/Open Source Options

| Tool | Type | Free Tier | Setup Time | Best For |
|------|------|-----------|------------|----------|
| **Cal.com** | Open source | Self-hosted | 2-4 hours | Full control |
| **Calendly** | SaaS | Basic free | 15 min | Simple scheduling |
| **Acuity** | SaaS | Free trial | 30 min | Service businesses |

## Option A: Cal.com (Self-Hosted, Full Control)

### Prerequisites
- Docker and Docker Compose
- 2GB RAM minimum
- Domain name (optional but recommended)

### Steps
```bash
# Clone Cal.com
git clone https://github.com/calcom/cal.com.git
cd cal.com

# Copy environment file
cp .env.example .env

# Edit .env with your settings:
# - DATABASE_URL (PostgreSQL)
# - NEXTAUTH_SECRET (random string)
# - NEXT_PUBLIC_WEBAPP_URL (your domain)

# Start with Docker
docker compose up -d

# Run database migrations
docker compose exec app npx prisma migrate dev

# Access at http://localhost:3000
```

### Configure
1. Create admin account
2. Set up event types (consultation, demo, support call)
3. Connect Google Calendar / Outlook
4. Configure availability (business hours, buffer time)
5. Set up email notifications
6. Get embed code for your website

### Embed on Website
```html
<!-- Inline embed -->
<iframe src="https://your-cal.com/your-user/30min" 
        width="100%" height="600" frameborder="0"></iframe>

<!-- Or popup button -->
<script>
  Cal("init", {origin:"https://your-cal.com"});
  Cal("inline", {
    elementOrSelector: "#my-calendar",
    calLink: "your-user/30min"
  });
</script>
```

## Option B: Calendly (Fastest)

### Steps
1. Sign up at https://calendly.com (free tier)
2. Set your availability
3. Create event types
4. Connect your calendar
5. Copy the embed code
6. Add to your website

## Integration Patterns

### Pattern 1: Service Booking
```
Customer visits site → Clicks "Book Consultation"
  → Sees available slots (synced with your calendar)
  → Selects time
  → Enters name, email, phone
  → Receives confirmation email + calendar invite
  → Receives reminder 24h before
  → Receives reminder 1h before
```

### Pattern 2: Automated Follow-up
```
After appointment → AI sends thank you email
  → Asks for feedback
  → Offers next appointment
  → Adds to CRM
```

## Best Practices
1. **Limit slots** — Don't show more than 2 weeks ahead
2. **Buffer time** — Add 15min between appointments
3. **Timezone** — Auto-detect customer timezone
4. **Reminders** — Send 24h and 1h before
5. **Cancellation** — Allow easy rescheduling
6. **Mobile** — Most bookings happen on mobile

## Pitfalls
- Don't over-complicate — start with one event type
- Don't forget to sync with your actual calendar
- Don't skip reminders — no-shows cost money
- Don't make customers create an account to book

## Testing Checklist
- [ ] Booking page loads on website
- [ ] Available slots match your calendar
- [ ] Confirmation email received
- [ ] Calendar invite received
- [ ] Reminder emails sent
- [ ] Cancellation/reschedule works
- [ ] Mobile responsive

## Verification
```bash
# Test Cal.com API (self-hosted)
curl -s https://your-cal.com/api/health | python3 -m json.tool

# Test booking flow
curl -s -X POST https://your-cal.com/api/book \
  -H "Content-Type: application/json" \
  -d '{"eventTypeId": 1, "start": "2026-06-15T10:00:00Z"}'
```
