# URL Shortener Service

> Converts long URLs → short trackable links with security & analytics.

---

## Quick Start (3 Steps)

| Step | Command | What Happens |
|:----:|---------|--------------|
| 1 | `pip install -r requirements.txt` | Installs 4 packages |
| 2 | `python main.py` | Starts server on port 8000 |
| 3 | Open `http://localhost:8000/docs` | Interactive API playground (Swagger UI) |

**Run tests:** `pytest tests/ -v` → 26 tests, all pass

---

## What I Built

```
Long URL ──→ [ URL Shortener ] ──→ Short Link + Analytics
                                        │
                                        ├── Click tracking
                                        ├── Access control
                                        └── Security checks
```

---

## Features (3 Groups)

| Group | Scenario | Features | In One Line |
|-------|----------|----------|-------------|
| **CORE** | Greenfield (built from scratch) | Create, Redirect, Analytics, List, Delete | "Basic URL shortener" |
| **ACCESS CONTROL** | Brownfield (added to existing) | Click limit, Expiration, Password, Bulk | "Who can access it" |
| **SECURITY** | Ambiguous (vague → clarified) | Rate limiting, URL blocking | "Prevent abuse" |

---

## Features at a Glance

| # | Feature | What It Does | Test It |
|:-:|---------|--------------|---------|
| 1 | **Shorten URL** | `https://long-url.com/page` → `localhost:8000/abc123` | POST `/api/urls` |
| 2 | **Custom Code** | Choose your own short code (e.g. `/sale2026`) | `"custom_code": "sale2026"` |
| 3 | **Redirect** | Visit short link → goes to original URL | GET `/{code}` in browser |
| 4 | **Analytics** | See who clicked, when, how many times | GET `/api/urls/{code}/analytics` |
| 5 | **Click Limit** | Link dies after N clicks | `"max_clicks": 5` |
| 6 | **Expiration** | Link dies after X hours | `"expires_in_hours": 48` |
| 7 | **Password** | Only people with password can access | `"password": "secret"` |
| 8 | **Bulk Create** | Create up to 50 links at once | POST `/api/urls/bulk` |
| 9 | **Rate Limit** | Blocks spam (max 10 requests/min) | Auto-enforced |
| 10 | **URL Blocking** | Rejects malicious/phishing domains | Auto-enforced |

---

## How to Test Each Feature

### Core (Greenfield — built from scratch)

```bash
# Create a short URL
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com", "custom_code": "goog"}'

# Visit it → redirects to Google
curl -L http://localhost:8000/goog

# See analytics (who clicked, when)
curl http://localhost:8000/api/urls/goog/analytics

# List all URLs
curl http://localhost:8000/api/urls

# Delete it
curl -X DELETE http://localhost:8000/api/urls/goog
```

### Access Control (Brownfield — added to existing system)

```bash
# Click Limit — stops after 3 clicks
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "limited", "max_clicks": 3}'
# Click 4th time → 404 "click limit reached"

# Expiration — dies after 2 hours
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/sale", "expires_in_hours": 2}'

# Password Protection — needs password to access
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://secret-doc.com", "custom_code": "secret", "password": "pass123"}'
# Access: curl http://localhost:8000/secret?password=pass123
# Without password → 401, wrong password → 403

# Bulk Create — multiple URLs at once
curl -X POST http://localhost:8000/api/urls/bulk \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://google.com", "https://github.com", "https://python.org"]}'
```

### Security (Ambiguous — requirement was vague, I clarified it)

```bash
# Rate Limiting — create 11 URLs rapidly → 11th gets rejected
# Returns: 429 "Rate limit exceeded"

# URL Blocking — try a malicious domain
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -d '{"url": "https://malware.com/steal"}'
# Returns: 409 "URL is blocked"
```

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   routes.py  │────▶│  service.py  │────▶│ database.py  │
│  (API Door)  │     │   (Brain)    │     │(Filing Cabinet)│
└──────────────┘     └──────────────┘     └──────────────┘
  Receives            Does the work:        Stores data:
  requests,           - Generate codes      - urls table
  sends               - Check limits        - clicks table
  responses           - Verify passwords    - rate_limits table
```

| Layer | File | Responsibility |
|-------|------|---------------|
| Entry Point | `main.py` | Starts the app |
| API | `app/routes.py` | 8 endpoints, rate limit check |
| Logic | `app/service.py` | All business rules |
| Data | `app/database.py` | SQLite (3 tables) |
| Validation | `app/models.py` | Input validation (Pydantic) |
| Tests | `tests/test_api.py` | 26 automated tests |

---

## Tech Stack

| What | Choice | Why |
|------|--------|-----|
| Language | Python | Simple, readable |
| Framework | FastAPI | Auto-generates API docs |
| Database | SQLite | Zero setup, portable file |
| Testing | Pytest | Fast, simple |
| Validation | Pydantic | Auto-rejects bad input |

---

## API Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| POST | `/api/urls` | Create short URL | 201 + short link |
| POST | `/api/urls/bulk` | Create many at once | 201 + list |
| GET | `/api/urls` | List all URLs | 200 + paginated list |
| GET | `/api/urls/{code}/analytics` | Click stats | 200 + analytics |
| DELETE | `/api/urls/{code}` | Remove a URL | 204 |
| GET | `/{code}` | Redirect to original | 301 redirect |
| POST | `/{code}/unlock` | Unlock password link | 200 + URL |
| GET | `/api/health` | Health check | 200 |

---

## Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 401 | Password required | Accessing protected link without password |
| 403 | Wrong password | Incorrect password provided |
| 404 | Not found | Expired, deleted, or click limit reached |
| 409 | Conflict | Duplicate code or blocked domain |
| 422 | Invalid input | Bad URL format |
| 429 | Too many requests | Rate limit exceeded (10/min) |

---

---

## Folder Structure

```
hemanth/
├── main.py              ← RUN THIS (starts the app)
├── requirements.txt     ← Dependencies (pip install)
├── app/
│   ├── routes.py        ← API endpoints
│   ├── service.py       ← Business logic
│   ├── database.py      ← Database setup
│   └── models.py        ← Input validation
├── tests/
│   └── test_api.py      ← 26 automated tests
└── docs/
    ├── SUBMISSION_OVERVIEW.md  ← Start here (evaluators)
    ├── APPROACH.md             ← How I solved it
    ├── DECISIONS.md            ← Trade-offs made
    ├── AI_USAGE.md             ← How AI helped
    ├── SCENARIOS.md            ← All 3 scenarios tested
    └── API_CONTRACT.md         ← Full API reference
```

---

## Documentation

| Doc | What's Inside |
|-----|--------------|
| [SUBMISSION_OVERVIEW.md](docs/SUBMISSION_OVERVIEW.md) | Maps every assignment requirement to files |
| [APPROACH.md](docs/APPROACH.md) | Step-by-step problem breakdown |
| [DECISIONS.md](docs/DECISIONS.md) | Key decisions + trade-offs |
| [AI_USAGE.md](docs/AI_USAGE.md) | AI contribution + 6 mistakes caught |
| [SCENARIOS.md](docs/SCENARIOS.md) | All 3 scenario types with curl commands |
| [API_CONTRACT.md](docs/API_CONTRACT.md) | Full API reference + DB schema |
