# Deliverables — How Each One Is Addressed

---

## Deliverable 1: Working Prototype

### Runnable Solution

| What | How |
|------|-----|
| Start command | `python main.py` |
| Interactive UI | `http://localhost:8000/docs` (Swagger) |
| No external setup | No Docker, no database install, no cloud |
| Works on | Any machine with Python 3.11+ |

### Accepts a Requirement → Produces Structured Outputs

| Requirement Given | What Was Produced |
|-------------------|-------------------|
| "Build URL shortener with APIs, persistence, analytics" | 5 Python files, 8 API endpoints, 3 database tables |
| "Add access control features" | Click limit, expiration, password protection, bulk create |
| "Make it more secure" | Rate limiting + URL domain blocking |

### URL Shortener Use Case — Demonstrated

| Input | Output |
|-------|--------|
| Long URL: `https://www.google.com/search?q=very+long+url` | Short link: `localhost:8000/abc123` |
| Visit short link | Redirects to original URL |
| Check analytics | Shows: 5 clicks, mostly from Chrome, peak on Monday |

---

## Deliverable 2: Architecture Overview

### System Design

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   routes.py  │────▶│  service.py  │────▶│ database.py  │
│  (API Door)  │     │   (Brain)    │     │(Filing Cabinet)│
└──────────────┘     └──────────────┘     └──────────────┘
```

| Layer | File | What It Does |
|-------|------|-------------|
| API Layer | `routes.py` | Receives HTTP requests, sends responses |
| Business Logic | `service.py` | All rules: generate codes, check limits, verify passwords |
| Data Layer | `database.py` | Stores/retrieves data from SQLite |
| Validation | `models.py` | Rejects bad input before it reaches the logic |

### How AI Tools Are Integrated Into Development Tasks

```
┌─────────────────────────────────────────────────┐
│              MY DEVELOPMENT PROCESS              │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. I define the task                           │
│         ↓                                       │
│  2. AI generates initial code                   │
│         ↓                                       │
│  3. I review — is it correct? secure? simple?   │
│         ↓                                       │
│  4. I fix issues (found 6 AI mistakes)          │
│         ↓                                       │
│  5. I test (26 automated tests)                 │
│         ↓                                       │
│  6. I validate (manual + Swagger UI)            │
│                                                 │
│  AI assists steps 2 only.                       │
│  I own steps 1, 3, 4, 5, 6.                    │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions and Trade-offs

| Decision | Chose | Over | Why |
|----------|-------|------|-----|
| Database | SQLite | PostgreSQL | Zero setup, portable, demo-friendly |
| Framework | FastAPI | Flask | Auto-generates interactive API docs |
| Short codes | Built-in `random` | External library | No install issues, no dependency |
| Passwords | SHA-256 | Plain text | Security (AI initially suggested plain text) |
| Delete | Soft delete | Hard delete | Audit trail preserved |
| Redirect | 302 | 301 | Browser doesn't cache, click tracking works |
| Rate limit | SQLite table | Redis | No extra service to install |
| Blocklist | Static list | External API | Works offline, no API key needed |

---

## Deliverable 3: Example Scenarios

---

### Scenario A: Greenfield Requirement

**Requirement:** "Build a URL shortener service with APIs, persistence, and analytics"

#### Task Breakdown

| # | Task | AI Assisted? |
|:-:|------|:------------:|
| 1 | Design database schema | Yes — generated SQL |
| 2 | Build CRUD service functions | Yes — generated boilerplate |
| 3 | Create REST API endpoints | Yes — generated route code |
| 4 | Add click tracking | Yes — generated insert logic |
| 5 | Build analytics query | Yes — generated SQL aggregation |
| 6 | Write tests | Yes — generated structure |

#### AI-Assisted Execution

| What I Asked AI | What AI Gave | What I Changed |
|-----------------|-------------|----------------|
| "Create SQLite table for URLs" | 10-column table | Simplified to 8 columns |
| "Generate FastAPI CRUD endpoints" | 4 basic endpoints | Added proper error codes + rate limit check |
| "Write analytics SQL query" | Basic COUNT query | Added GROUP BY date + recent clicks |

#### Output Validation

| Check | Method | Result |
|-------|--------|--------|
| Create URL works | Automated test + Swagger | ✓ Returns 201 + short code |
| Redirect works | Browser test | ✓ Goes to original URL |
| Analytics accurate | Created URL, clicked 3x, checked count | ✓ Shows 3 |
| Duplicate rejected | Created same code twice | ✓ Returns 409 |
| Invalid URL rejected | Sent "not-a-url" | ✓ Returns 422 |

---

### Scenario B: Brownfield Requirement

**Requirement:** "Add click limit, expiration, and password protection to the existing URL shortener"

#### Task Breakdown

| # | Task | Depends On | AI Assisted? |
|:-:|------|:----------:|:------------:|
| 1 | Add `max_clicks` column to existing schema | Existing DB | Yes |
| 2 | Add `expires_at` column | Existing DB | Yes |
| 3 | Add `password` column | Existing DB | Yes |
| 4 | Modify redirect to check limits before allowing | Existing redirect | Yes |
| 5 | Add password verification logic | Existing service | Partial (I fixed hashing) |
| 6 | Add bulk creation endpoint | Existing create | Yes |
| 7 | Update tests (don't break old ones) | Existing tests | Yes |

#### AI-Assisted Execution

| What I Asked AI | What AI Gave | What I Changed |
|-----------------|-------------|----------------|
| "Add click limit check before redirect" | Basic if/else | Added proper 404 message |
| "Add password to URL creation" | Plain text storage! | Fixed → SHA-256 hashing |
| "Add bulk endpoint" | Loop with no error handling | Added per-URL error handling |

#### Output Validation

| Check | Method | Result |
|-------|--------|--------|
| Click limit works | Clicked 3x (works), 4th time (404) | ✓ |
| Expiration works | Created 15-sec link, waited, tried again | ✓ 404 after expiry |
| Password blocks | Accessed without password | ✓ Returns 401 |
| Wrong password | Entered wrong password | ✓ Returns 403 |
| Correct password | Entered right password | ✓ Redirects |
| Old features still work | Ran all 26 tests | ✓ All pass |

**Key Brownfield Challenge:** Adding new features WITHOUT breaking existing functionality. All original tests still pass after adding new features.

---

### Scenario C: Ambiguous Requirement

**Requirement:** "The URL shortener needs to be more secure"

#### Clarification Process

| Step | What I Did |
|------|-----------|
| 1 | Identified ambiguity: "secure" can mean 20 different things |
| 2 | Asked: "Secure from what? What abuse do we expect?" |
| 3 | Narrowed to 2 real threats: spam bots + malicious URLs |
| 4 | Chose practical solutions within demo scope |

#### Task Breakdown

| # | Task | Decision Made By |
|:-:|------|:----------------:|
| 1 | Define "secure" — what threats? | Me (engineer) |
| 2 | Choose approach: rate limiting | Me (rejected AI's Redis suggestion) |
| 3 | Implement rate limit (10 req/min) | AI generated, I reviewed |
| 4 | Choose approach: URL blocking | Me (static list over external API) |
| 5 | Implement domain blocklist | AI generated, I reviewed |
| 6 | Test both features | Me + AI test structure |

#### AI-Assisted Execution

| What I Asked AI | What AI Gave | What I Changed |
|-----------------|-------------|----------------|
| "Add rate limiting" | Redis-based counter | Replaced with SQLite (no Redis needed) |
| "Block malicious URLs" | External API call | Replaced with static blocklist (works offline) |

#### Output Validation

| Check | Method | Result |
|-------|--------|--------|
| Rate limit blocks spam | Sent 11 requests in 1 min | ✓ 11th returns 429 |
| Allowed after window | Waited 60 sec, tried again | ✓ Works |
| Malicious URL blocked | Sent malware.com | ✓ Returns 409 |
| Safe URL allowed | Sent google.com | ✓ Returns 201 |

#### Trade-offs Documented

| Decision | Pro | Con |
|----------|-----|-----|
| IP-based rate limit | Simple, no auth needed | VPN users can bypass |
| Static blocklist | No external API, works offline | List gets outdated |
| No authentication | Easy to use | Anyone can create URLs |

---

## Deliverable 4: Setup Instructions

### Prerequisites

| What | Version | Check Command |
|------|---------|---------------|
| Python | 3.11 or higher | `python --version` |
| pip | Any | `pip --version` |

### Steps to Run

```bash
# Step 1: Install dependencies (one time, ~10 seconds)
pip install -r requirements.txt

# Step 2: Start the server
python main.py

# Step 3: Open in browser
# http://localhost:8000/docs
```

### Steps to Test

```bash
# Run all 26 automated tests
python -m pytest tests/ -v
```

### Steps to Evaluate

| What to Evaluate | Where to Look |
|------------------|---------------|
| Code quality | `app/` folder (4 files) |
| API design | `http://localhost:8000/docs` (live) |
| Test coverage | `tests/test_api.py` |
| Documentation | `docs/` folder |
| Architecture | `docs/SUBMISSION_OVERVIEW.md` |

### Fresh Start (Before Demo)

```bash
# Delete old test data
rm -rf data

# Start fresh
python main.py
```

---

## Deliverable 5: Testing Approach

### How Correctness Was Validated

| Method | What It Tests | Tool |
|--------|--------------|------|
| Syntax check | All files parse correctly | `py_compile` |
| Unit tests | Each function in isolation | `pytest` |
| Integration tests | Full request → response flow | `pytest` + `TestClient` |
| Manual testing | End-to-end user experience | Swagger UI |
| Edge case testing | Limits, boundaries, invalid input | Custom test cases |

### Test Coverage by Feature

| Feature | # Tests | Edge Cases Covered |
|---------|:-------:|-------------------|
| Create URL | 3 | Valid, invalid format, duplicate code |
| Redirect | 2 | Existing code, non-existing code |
| Analytics | 1 | Click count accuracy |
| List URLs | 1 | Pagination |
| Delete | 2 | Existing, non-existing |
| Click limit | 4 | Within limit, at limit, over limit, no limit |
| Expiration | 2 | Before expiry, after expiry |
| Password | 5 | No password, wrong, correct, unlock endpoint |
| Bulk create | 2 | Valid batch, invalid URL in batch |
| Rate limiting | 1 | Exceeds 10 requests |
| URL blocking | 2 | Malicious domain, safe domain |
| **Total** | **26** | — |

### How Test Isolation Works

```python
# Each test gets a fresh database (no interference between tests)
@pytest.fixture(autouse=True)
def fresh_db():
    # Delete old database
    # Create new tables
    # Run test
    # Clean up
```

### Known Limitations

| Limitation | Why It's Acceptable | How to Fix in Production |
|------------|-------------------|--------------------------|
| SQLite (not scalable) | Demo scope, works perfectly for evaluation | Swap to PostgreSQL |
| No authentication | Simplifies demo and testing | Add OAuth2 / API keys |
| Static URL blocklist (4 domains) | Demonstrates the concept | Integrate VirusTotal API |
| Rate limit bypassed with VPN | IP-based is simplest approach | Add token-based auth + Redis |
| No HTTPS | Running locally | Add Nginx + SSL certificate |
| No load testing | Out of scope for demo | Add Locust / k6 tests |

### Quality Assurance Summary

| QA Area | Status |
|---------|--------|
| All features work end-to-end | ✓ Verified in Swagger UI |
| All 26 tests pass | ✓ `pytest tests/ -v` |
| No SQL injection possible | ✓ Parameterized queries |
| Passwords never stored plain | ✓ SHA-256 hashed |
| Bad input rejected | ✓ Pydantic validation |
| Proper HTTP status codes | ✓ 201, 204, 302, 401, 403, 404, 409, 422, 429 |
| Code is modular and readable | ✓ 3-layer architecture |
