---
name: visual-audit
description: Analyze screenshots and images to identify UI issues. Use when you need to: check what's wrong in a screenshot, compare designs, find visual inconsistencies, audit colors/fonts/布局.
---

# Visual Audit Skill

## Use When

- User sends a screenshot showing a problem
- Need to compare two images
- Finding visual inconsistencies in the UI
- Auditing colors, fonts, spacing

## How to Analyze

### Step 1: Look at the Image
- Describe what you see
- Note colors, fonts, layout
- Identify the page/component

### Step 2: Compare to Expected
- What's different from the design?
- What colors are off?
- What elements are missing?

### Step 3: Identify Issues
- Color mismatches
- Font problems  
- Layout issues
- Spacing problems
- Duplicate links

### Step 4: Fix
- Tell the user what's wrong
- Make the fix
- Push to GitHub
- Update local repo

## Example

User: "The nav looks crazy - there are duplicate links"

Analysis:
1. Look: I see Dashboard, Add Product, Ads dropdown (correct), BUT also Ad Vault and Listing Generator showing as separate links
2. Problem: These are duplicated - they're in the dropdown AND showing separately
3. Fix: Remove the standalone links, keep only dropdown

## GitHub Workflow

```bash
# Pull latest
git pull origin main

# Make fix
sed -i 's|duplicate link||' template.html

# Push
git add -A && git commit -m "Fix visual issue" 
git push origin main
```

## Best Practices

- Always sync to GitHub frequently (every ~15 min when working fast)
- Update your local brain (Echo repo) too
- Make small, focused changes
- Test after each change