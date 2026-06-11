---
name: ai-marketing-agent
description: AI-powered marketing automation for small businesses — email campaigns, social media, ad creation, lead nurturing, all free tier
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Marketing Agent for Small Business

## When to use
- Automating email marketing campaigns
- Scheduling and creating social media content
- Creating ad copy and images
- Lead scoring and nurturing
- Marketing analytics and reporting

## Free/Open Source Options

| Tool | Type | Free Tier | Best For |
|------|------|-----------|----------|
| **Mailchimp** | SaaS | 500 contacts free | Email marketing |
| **Buffer** | SaaS | 3 channels free | Social media scheduling |
| **Mautic** | Open source | Self-hosted | Full marketing automation |
| **n8n** | Open source | Self-hosted | Workflow automation |

## Implementation Pattern

### Email Marketing (Mailchimp Free)
```
1. Sign up at mailchimp.com (free up to 500 contacts)
2. Import customer list
3. Create email template
4. Set up automation:
   - Welcome series (new subscribers)
   - Abandoned cart (e-commerce)
   - Re-engagement (inactive customers)
5. Schedule sends
6. Track open rates, click rates
```

### Social Media (Buffer Free)
```
1. Sign up at buffer.com (free: 3 channels, 10 scheduled posts)
2. Connect social accounts (Facebook, Instagram, Twitter)
3. Create content calendar
4. Schedule posts
5. Track engagement
```

### Full Automation (Mautic Self-Hosted)
```bash
# Install Mautic
git clone https://github.com/mautic/mautic.git
cd mautic
composer install
php bin/console mautic:install

# Access at http://localhost:8000
# Configure campaigns, forms, emails
```

## Best Practices
1. **Segment your list** — Send relevant content to each group
2. **Don't over-email** — 1-2 emails/week max
3. **Personalize** — Use names, past purchases, preferences
4. **A/B test** — Test subject lines, content, send times
5. **Track everything** — Know what works and what doesn't

## Pitfalls
- Don't spam — Unsubscribe rates hurt deliverability
- Don't ignore mobile — 60%+ of emails opened on mobile
- Don't forget CAN-SPAM — Include unsubscribe link
- Don't set and forget — Review analytics weekly

## Testing Checklist
- [ ] Email sends successfully
- [ ] Template renders correctly
- [ ] Links work
- [ ] Unsubscribe works
- [ ] Social posts schedule correctly
- [ ] Analytics tracking works
