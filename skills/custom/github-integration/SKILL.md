---
name: github-integration
description: Full GitHub integration - issues, PRs, actions, releases. Use when you need to create issues, manage PRs, trigger workflows, or interact with GitHub API.
---

# GitHub Integration

## Issues

```bash
# Create issue
gh issue create --title "Bug found" --body "Description"

# List issues
gh issue list --state all

# Close issue
gh issue close 123
```

## Pull Requests

```bash
# Create PR
gh pr create --title "Fix it" --body "How I fixed it"

# List PRs
gh pr list --state all

# Review PR
gh pr review 123 --approve
```

## Actions

```bash
# Run workflow
gh run run-workflow -n deploy

# Check status
gh run view
```

## API Calls

```bash
# List repos
gh api repos

# Get issues
gh api repos/owner/repo/issues

# Custom request
gh api -X POST repos/owner/repo/dispatches -f event="push"
```

## GraphQL

```bash
gh api graphql -f query='{viewer{login}}'
```

## Best Practices

- Use `--jq` to filter output
- Check `gh status` for context
- Use environment variables for auth