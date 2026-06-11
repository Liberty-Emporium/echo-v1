---
name: ai-voice-agent
description: AI voice agent for small business phone calls — answer calls, book appointments, qualify leads, handle FAQs 24/7 with natural speech
version: 1.0.0
platforms: [linux, macos]
status: UNTESTED
---

# AI Voice Agent for Small Business

## When to use
- Answering business phone calls 24/7
- Booking appointments via phone
- Qualifying leads before human handoff
- Filtering junk/spam calls
- Handling FAQ calls (hours, location, services)

## Key Stat
AI voice agents can answer phone calls in natural spoken language, book appointments, qualify leads, and handle FAQs around the clock (2026).

## Free/Open Source Options

| Tool | Type | Free Tier | Best For |
|------|------|-----------|----------|
| **Twilio** | API | Free trial ($15 credit) | Telephony backbone |
| **Vapi** | Platform | Free tier | Voice AI platform |
| **OpenVoice** | Open source | Self-hosted | Full control |

## Implementation Pattern

### Step 1: Set Up Telephony (Twilio)
```bash
# Sign up at https://twilio.com (free trial with $15 credit)
# Buy a phone number (~$1/month)
# Configure webhook for incoming calls
```

### Step 2: Configure Voice AI
```
Incoming Call → Twilio → Webhook → AI Voice Agent
  → Speech-to-text (Twilio STT or Whisper)
  → LLM processes intent
  → Text-to-speech response
  → Continue conversation or take action
```

### Step 3: Define Call Flows
```
Greeting: "Thank you for calling [Business]. How can I help you?"

Intents:
  - Book appointment → Check calendar → Confirm time → Send confirmation
  - Business hours → "We're open Monday-Friday 9 to 5..."
  - Location → "We're located at..."
  - Speak to human → Transfer to owner's phone
  - FAQ → Answer from knowledge base
```

## Best Practices
1. **Keep it natural** — Use conversational language, not robotic
2. **Offer human transfer** — Always give option to speak to a person
3. **Keep it short** — AI should resolve or transfer in < 2 minutes
4. **Log everything** — Record calls and transcriptions
5. **Test with real calls** — Have friends call and test

## Pitfalls
- Don't make it sound robotic — use natural TTS voices
- Don't trap callers in AI loops — always offer human
- Don't forget to test with accents and background noise
- Don't skip compliance — some states require call recording disclosure

## Testing Checklist
- [ ] Phone number receives calls
- [ ] AI greets callers naturally
- [ ] Intent recognition works
- [ ] Appointment booking works
- [ ] Human transfer works
- [ ] Call logging works
- [ ] Voicemail fallback works

## Verification
```bash
# Test Twilio webhook
curl -X POST https://your-server.com/voice/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "CallSid=test123&From=%2B1234567890&To=%2B1987654321"
```
