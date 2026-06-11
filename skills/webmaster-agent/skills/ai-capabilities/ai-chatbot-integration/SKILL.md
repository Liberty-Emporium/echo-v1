---
name: ai-chatbot-integration
description: Set up an AI-powered customer service chatbot on a small business website — free tier, open source options, CRM integration, and human escalation
version: 1.0.0
platforms: [linux, macos, websites]
status: UNTESTED
---

# AI Chatbot Integration for Small Business

## When to use
- Adding customer service chatbot to a small business website
- Automating FAQ responses
- Handling order inquiries
- Qualifying leads before human handoff

## Key Stat
AI chatbots now handle **70% of repetitive customer queries** without human intervention (2026 data).

## Free/Open Source Options Comparison

| Tool | Type | Free Tier | Setup Time | Best For |
|------|------|-----------|------------|----------|
| **Tawk.to** | SaaS | Unlimited free | 15 min | Quick setup, live chat + bot |
| **Botpress** | Open source | Self-hosted | 2-4 hours | Full control, custom AI |
| **OpenAssistantGPT** | Open source | Self-hosted | 1-2 hours | GPT-4 powered, no-code |
| **Tidio** | SaaS | Free plan | 30 min | E-commerce integration |
| **Crisp** | SaaS | Free plan | 30 min | Team inbox + chatbot |

## Option A: Tawk.to (Fastest — 15 minutes)

### Steps
1. Sign up at https://tawk.to (free, no credit card)
2. Create a new property for your website
3. Copy the embed code
4. Add to your website's `<head>` or before `</body>`:
```html
<!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/YOUR_PROPERTY_ID/default';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
<!--End of Tawk.to Script-->
```
5. Configure the chatbot in Tawk.to dashboard:
   - Set greeting message
   - Add FAQ responses
   - Set offline message
   - Configure notification email

### Verification
- Visit your website
- Click the chat widget
- Send a test message
- Verify you receive notification

## Option B: Botpress (Full Control — Self-Hosted)

### Prerequisites
- Node.js 18+
- 2GB RAM minimum
- Linux server or VPS

### Steps
```bash
# Install Botpress
npx botpress init my-chatbot
cd my-chatbot
npx botpress start

# Access the studio at http://localhost:3000
```

### Configure
1. Create intents (greeting, FAQ, order_status, human_handoff)
2. Add training phrases for each intent
3. Create responses
4. Connect to your website via the embed code Botpress provides

### Verification
- Test each intent in the Botpress emulator
- Verify responses are accurate
- Test the embed on your website

## Option C: OpenAssistantGPT (GPT-4 Powered)

### Steps
1. Clone the repo:
```bash
git clone https://github.com/OpenAssistantGPT/OpenAssistantGPT.git
cd OpenAssistantGPT
```
2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```
3. Run:
```bash
npm install
npm run build
npm start
```
4. Upload your FAQ documents
5. Get embed code and add to website

## Integration Patterns

### Pattern 1: FAQ Bot
```
Customer: "What are your hours?"
→ AI: "We're open Monday-Friday 9AM-5PM, Saturday 10AM-4PM, closed Sunday."

Customer: "Do you ship to Canada?"
→ AI: "Yes! We ship to Canada for $15 flat rate. Delivery takes 5-7 business days."
```

### Pattern 2: Order Status
```
Customer: "Where is my order #12345?"
→ AI: [Checks order API] "Your order #12345 is out for delivery. Expected today by 5PM."
```

### Pattern 3: Lead Qualification
```
Customer: "I'm interested in your services"
→ AI: "Great! What type of service are you looking for?"
→ AI: [Collects info] → Routes to sales team with context
```

### Pattern 4: Human Escalation
```
Customer: "I need to speak to a manager"
→ AI: "I'll connect you with a team member. Please hold..."
→ [Routes to human agent with full conversation context]
```

## Best Practices

1. **Set clear expectations** — Tell customers they're chatting with AI
2. **Keep responses short** — 2-3 sentences max
3. **Always offer human escalation** — "Would you like to speak to a person?"
4. **Train on real data** — Use actual customer questions
5. **Monitor and improve** — Review chat logs weekly
6. **Multilingual** — Add Spanish, French if your customers need it
7. **Mobile-first** — Most customers will use mobile

## Pitfalls
- Don't pretend the AI is human — be transparent
- Don't rely on AI for complex issues — always offer human escalation
- Don't forget to update FAQs when business changes
- Don't ignore chat logs — they're gold for improving service
- Don't set and forget — monitor weekly

## Testing Checklist
- [ ] Chat widget appears on website
- [ ] Greeting message displays correctly
- [ ] FAQ responses are accurate
- [ ] Order lookup works (if applicable)
- [ ] Human escalation works
- [ ] Mobile responsive
- [ ] Notifications received
- [ ] Multilingual works (if configured)

## Verification Command
```bash
# Test chatbot API endpoint (if self-hosted)
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your hours?"}'

# Expected: JSON response with answer
```
