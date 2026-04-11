---
name: internet-researcher
description: Search the web, fetch URLs, summarize content, and gather information. Use when you need to look up facts, research topics, find documentation, or get current information from the internet.
---

# Internet Researcher

## Capabilities

### 1. Web Search (`web_search`)

Search DuckDuckGo for information. Good for:
- Quick facts
- Finding documentation
- Looking up error messages
- Current events
- Comparison shopping

```bash
# Usage is automatic via tool call
web_search query="your search query"
```

**Tips:**
- Be specific: "Python Flask JSONify list" not "Flask JSON"
- Include context: "FastAPI vs Flask performance 2024"
- For code/errors: include exact error message

### 2. Web Fetch (`web_fetch`)

Fetch and extract readable content from URLs. Good for:
- Reading articles
- Extracting documentation
- Pulling data from APIs
- Summarizing long pages

```bash
# Usage is automatic via tool call
web_fetch url="https://example.com"
```

**Tips:**
- Works with most HTTP/HTTPS URLs
- Returns markdown-formatted text
- Use `maxChars` to limit output for very long pages

### 3. Summarize (`summarize` skill)

Use the `summarize` skill for:
- YouTube/video transcripts
- Podcast summaries
- Long-form content extraction
- Extracting key points from articles

## Research Workflow

### For Fact Checking
1. Web search the claim
2. Check multiple sources
3. Note_conflicting information

### For Learning a Topic
1. Web search for overview
2. Web fetch top 2-3 results
3. Synthesize into summary

### For Documentation
1. Web search "[topic] documentation"
2. Web fetch official docs
3. Extract relevant sections

### For Current Info
1. Web search with date indicator
2. Note when sources were published
3. Check for newer updates

## Best Practices

- **Verify with multiple sources** - Don't trust a single result
- **Check dates** - Information can go stale
- **Bookmark useful URLs** - Save for later reference
- **Use specific queries** - "how to X in language" beats "how to X"

## Common Patterns

### Error Resolution
```
1. Search: "[exact error message]"
2. Look for Stack Overflow, GitHub issues
3. Try accepted solutions
4. Test and verify
```

### Learning New Tech
```
1. Search: "[technology] getting started"
2. Fetch official documentation
3. Search tutorials
4. Build small example
```

### Product/Tool Comparison
```
1. Search: "[tool A] vs [tool B]"
2. Fetch detailed comparisons
3. Check recent discussions (Reddit, Hacker News)
4. Consider your specific use case
```

## Notes

- `web_search` uses DuckDuckGo (no API key needed)
- Some sites may block fetching
- Rate limiting: be reasonable with requests
- `web_fetch` max: ~50KB per call