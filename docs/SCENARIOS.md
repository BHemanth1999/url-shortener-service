# Example Scenarios

All scenarios are implemented in the code and testable live.

---

## Scenario 1: Greenfield — Build URL Shortener

**Requirement:** "Build a scalable URL shortener service with APIs, persistence, and analytics."

### What was built
- Create short URLs (auto or custom code)
- Redirect with 301
- Click analytics (count, dates, recent visitors)
- List all URLs (paginated)
- Soft delete

### How to test
```bash
# Create
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com", "custom_code": "goog"}'

# Redirect (browser): http://localhost:8000/goog → goes to Google

# Analytics
curl http://localhost:8000/api/urls/goog/analytics

# List all
curl http://localhost:8000/api/urls

# Delete
curl -X DELETE http://localhost:8000/api/urls/goog
```

### Validation
- 12 tests cover core functionality
- Invalid URLs → 422
- Duplicate codes → 409
- Missing URLs → 404

---

## Scenario 2: Brownfield — Enhancement Features

### 2a. Click Limit

**Requirement:** "Add maximum click limit — URL stops working after N clicks."

**Use case:** Share a research report with only 50 clients.

```bash
# Create with limit of 3 clicks
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "limited", "max_clicks": 3}'

# Click 1, 2, 3 → redirect works
# Click 4 → 404 "click limit reached"

# Check remaining in analytics
curl http://localhost:8000/api/urls/limited/analytics
# Shows: "max_clicks": 3, "clicks_remaining": 0
```

---

### 2b. URL Expiration

**Requirement:** "URLs should auto-expire after a set time period."

**Use case:** Time-limited promotional offer link (48-hour sale).

```bash
# Create link that expires in 2 hours
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/sale", "custom_code": "sale48", "expires_in_hours": 2}'

# Works now → redirect
# After 2 hours → 404 "expired"

# Analytics shows expiry status
curl http://localhost:8000/api/urls/sale48/analytics
# Shows: "expires_at": "2026-07-30 14:00:00", "is_expired": false
```

---

### 2c. Password Protection

**Requirement:** "Some links should require a password to access."

**Use case:** Secure document sharing (only people with password can open).

```bash
# Create password-protected link
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://secret-doc.com", "custom_code": "secret", "password": "pass123"}'

# Try without password → 401 "password required"
curl http://localhost:8000/secret

# With correct password → redirect works
curl http://localhost:8000/secret?password=pass123

# With wrong password → 403 "wrong password"
curl http://localhost:8000/secret?password=wrong

# Alternative: POST unlock endpoint
curl -X POST http://localhost:8000/secret/unlock \
  -H "Content-Type: application/json" \
  -d '{"password": "pass123"}'
```

---

### 2d. Bulk Creation

**Requirement:** "Marketing team needs to create many short URLs at once."

**Use case:** Campaign launch with 50 product links.

```bash
# Create 3 URLs at once
curl -X POST http://localhost:8000/api/urls/bulk \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://github.com", "https://python.org"], "expires_in_hours": 72}'

# Response shows all created URLs with their short codes
```

---

## Scenario 3: Ambiguous — "Make it More Secure"

**Requirement:** "The URL shortener needs to be more secure."

### Clarification process
- "Secure from what?" → Spam and malicious links
- "What kind of abuse?" → Bots creating thousands of links + phishing URLs

### What was built

**1. Rate Limiting** (10 requests per minute per IP)
```bash
# Create 11 URLs rapidly → 11th returns:
# 429 "Rate limit exceeded. Max 10 requests per minute."
```

**2. URL Blocking** (rejects known malicious domains)
```bash
# Try a malicious URL
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://malware.com/steal-data"}'
# Returns: 409 "URL is blocked - domain is not allowed"

# Safe URL works fine
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
# Returns: 201 Created
```

### Trade-offs
| Decision | Pro | Con |
|----------|-----|-----|
| IP-based rate limit | Simple, no auth needed | VPN bypass possible |
| Static blocklist | No external API | List becomes outdated |
| No authentication | Easy to use | Anyone can create/delete |

---

## Summary

| Scenario | Feature | Tests | Status |
|----------|---------|:-----:|:------:|
| Greenfield | Core CRUD + analytics | 12 | ✅ |
| Brownfield | Click limit | 4 | ✅ |
| Brownfield | URL expiration | 2 | ✅ |
| Brownfield | Password protection | 5 | ✅ |
| Brownfield | Bulk creation | 2 | ✅ |
| Ambiguous | Rate limiting + URL blocking | 2 | ✅ |
| **Total** | | **26** | **All pass** |
