# Compaction Guide

Worked examples and edge case patterns for markdown compaction. Read when compacting non-trivial files or when unsure how to handle a specific construct.

---

## Worked Example

### Before (38 lines)

```markdown
# API Authentication Guide

## Introduction

This guide provides a comprehensive overview of the authentication
mechanisms available in our API. It is important to note that all
endpoints require authentication unless otherwise specified.

## Authentication Methods

### API Key Authentication

In order to authenticate using an API key, you need to include
the `X-API-Key` header in your request.

**Example:**

```
curl -H "X-API-Key: your-key" https://api.example.com/users
```

**Another example with query parameter:**

```
curl https://api.example.com/users?api_key=your-key
```

### OAuth 2.0

OAuth 2.0 is a more secure authentication method. It is recommended
for applications that need to access user data on behalf of the user.

#### Supported Grant Types

- **Authorization Code** — Used for server-side applications. This is the most common and most secure grant type available.
- **Client Credentials** — Used for machine-to-machine communication. This grant type is suitable when the application needs to access its own resources.
- **Refresh Token** — Used to obtain a new access token when the current one expires. This is important for maintaining long-lived sessions.

## Rate Limiting

All authenticated requests are subject to rate limiting. The current
limits are as follows:

- **Free tier**: 100 requests per minute
- **Pro tier**: 1,000 requests per minute
- **Enterprise tier**: 10,000 requests per minute

If you exceed the rate limit, you will receive a `429 Too Many Requests`
response. In that case, you should wait before retrying.
```

### After (18 lines)

```markdown
# API Authentication

All endpoints require authentication unless noted.

## Methods

### API Key

Include `X-API-Key` header:
```
curl -H "X-API-Key: your-key" https://api.example.com/users
```

### OAuth 2.0

Supported grant types:
- **Authorization Code** — server-side apps
- **Client Credentials** — machine-to-machine
- **Refresh Token** — renew expired access tokens

## Rate Limits

| Tier | Limit |
|------|-------|
| Free | 100 req/min |
| Pro | 1,000 req/min |
| Enterprise | 10,000 req/min |

Exceeding the limit returns `429`. Wait before retrying.
```

### What each pass did

| Pass | Changes |
|------|---------|
| **Collapse** | Removed "Introduction" section — restated the title. Merged single-item "Supported Grant Types" into parent. |
| **Terse** | "It is important to note that" → removed. "In order to" → removed. "provides a comprehensive overview of" → removed. Grant type descriptions trimmed to essentials. |
| **Trim examples** | Removed query parameter example (same point as header example). |
| **Symbols** | No changes needed — no opportunities. |
| **Formatting** | Converted rate limits from bullet list to table (denser, scannable). Removed decorative bold from "Example:" labels. |

**Result**: 38 → 18 lines (53% reduction), zero information loss.

---

## Edge Cases

### Tables

Tables are already dense. Do not try to compact them further unless:
- A column contains identical values in most rows → remove column, state the default once above
- Headers repeat content from a section heading → shorten headers

```markdown
# Before — redundant column
| Method | Auth Required | Rate Limited |
|--------|--------------|-------------|
| GET /users | Yes | Yes |
| POST /users | Yes | Yes |
| GET /health | No | No |

# After — default stated, exceptions listed
All endpoints require auth and rate limiting except:
- `GET /health` — no auth, no rate limit
```

### Nested lists

Flatten lists deeper than 2 levels. Convert the third level into a parenthetical or separate sentence.

```markdown
# Before (3 levels)
- Authentication
  - OAuth
    - Authorization Code
    - Client Credentials
  - API Key

# After (2 levels)
- Authentication: OAuth (Authorization Code, Client Credentials) or API Key
```

### YAML frontmatter

Never modify YAML frontmatter content. The `description` field is consumed by tooling and must remain semantically identical. Compaction rules apply only below the closing `---`.

### Code blocks

Preserve code blocks exactly — no compaction inside fences. The one exception: detected credentials are redacted per the credential scan pass.

If multiple code blocks illustrate the same point, keep the most complete one and remove the rest.

### Inline code

Never alter inline code (`backtick` content). It may be a command, path, or identifier where exact characters matter.

### Links and references

Preserve all URLs. If a link's display text is verbose, shorten the display text but keep the URL:

```markdown
# Before
[Click here to read the full documentation on authentication](https://docs.example.com/auth)

# After
[Auth docs](https://docs.example.com/auth)
```

### Headings as structure

Keep headings unless the section is fully absorbed into another. Headings serve as navigation anchors — removing them hurts scannability even if the content is merged.

### Credential patterns to catch

The credential scan (pass 1) should flag these patterns inside any context — prose, code blocks, inline code, YAML:

| Pattern | Example |
|---------|---------|
| API keys | `sk-proj-...`, `AKIA...`, `ghp_...`, `xoxb-...` |
| Tokens | `Bearer eyJ...`, `token: abc123def456` |
| Connection strings | `postgres://user:pass@host/db`, `mongodb+srv://...` |
| Private keys | `-----BEGIN RSA PRIVATE KEY-----` |
| Passwords in config | `password: ...`, `secret: ...`, `DB_PASSWORD=...` |

When in doubt, flag it. A false positive costs the user a confirmation; a missed credential costs a leak.
