# Evaluation Criteria — How I Demonstrated Each One

---

## Mandatory Use Case

> "Build a scalable URL shortener service with APIs, persistence, and analytics."

### How I Broke Down the Requirement

```
Original: "Build a scalable URL shortener service with APIs, persistence, and analytics"
                    │              │          │              │              │
                    ▼              ▼          ▼              ▼              ▼
              Design for      8 REST      SQLite       Click count     Future-ready
              growth         endpoints    3 tables     by date/IP      architecture
```

| Word in Requirement | My Interpretation | What I Built |
|---------------------|-------------------|--------------|
| "Scalable" | Can handle more features without rewriting | 3-layer architecture (swap any layer independently) |
| "URL shortener" | Long URL → short code → redirect | Create + redirect + custom codes |
| "APIs" | REST endpoints with proper HTTP standards | 8 endpoints, proper status codes, OpenAPI spec |
| "Persistence" | Data survives server restart | SQLite database (3 tables) |
| "Analytics" | Track who clicked, when, how many | Click count, clicks by date, visitor info |

### How AI Assisted Each Component

| Component | AI Contribution | My Contribution |
|-----------|----------------|-----------------|
| Database schema | Generated CREATE TABLE SQL | Decided 3 tables, column types, relationships |
| API endpoints | Generated FastAPI route decorators | Decided URL structure, HTTP methods, error codes |
| Business logic | Generated function bodies | Decided what each function does, added edge cases |
| Short code generation | Suggested `shortuuid` library | Rejected → used built-in `random` (no dependency) |
| Click tracking | Generated INSERT query | Decided what to track (IP, user agent, referrer, time) |
| Analytics queries | Generated basic COUNT | Added GROUP BY date, recent clicks, remaining clicks |
| Tests | Generated test structure | Added 10+ edge cases AI missed |

### Code, APIs, and Tests Generated

| Output Type | Quantity | Quality Check |
|-------------|----------|---------------|
| Python files | 5 files, ~535 lines | Modular, readable, no code smells |
| API endpoints | 8 RESTful endpoints | Proper HTTP codes, OpenAPI auto-docs |
| Database | 3 tables, proper foreign keys | Normalized, indexed, efficient |
| Tests | 26 automated tests | Cover all features + edge cases |
| Documentation | 10 markdown files | Every requirement addressed |

### Validation and Trade-offs Provided

| What I Validated | How | Result |
|------------------|-----|--------|
| Code syntax | `py_compile` all files | All pass |
| Logic correctness | 26 automated tests | All pass |
| API correctness | Manual Swagger UI testing | All endpoints work |
| Security | Reviewed SQL queries, password handling | Parameterized queries, hashed passwords |
| Edge cases | Expired links, wrong passwords, limits | All handled properly |

| Trade-off Made | Why |
|----------------|-----|
| SQLite over PostgreSQL | Portability > scalability for demo |
| No auth | Simplicity > production-readiness for demo |
| Static blocklist | Offline capability > real-time accuracy |
| SHA-256 over bcrypt | No extra library > maximum security |

---

## Evaluation Criteria — My Evidence

---

### 1. Effective Use of AI Tools in Development Tasks

| Evidence | Where to See It |
|----------|----------------|
| AI used for ALL development tasks | `docs/AI_USAGE.md` — table of AI vs Engineer per task |
| Clear prompting examples | `docs/CORE_REQUIREMENTS_MAPPING.md` — Section 3 |
| AI suggestions accepted AND rejected | 5 accepted patterns, 5 rejected suggestions |
| Iterative refinement shown | Password: plain text → hashed → verified (3 rounds) |

**My Approach:**
```
I used AI like a junior developer on my team:
  - I tell it WHAT to build
  - It writes the first draft
  - I review, test, fix, and approve
  - I take full responsibility for the final code
```

---

### 2. Strength of Software Design and Implementation

| Design Principle | How I Applied It |
|------------------|-----------------|
| **Separation of concerns** | Routes handle HTTP, Service handles logic, Database handles storage |
| **Single responsibility** | Each file does one thing only |
| **Input validation** | Pydantic rejects bad data before it reaches logic |
| **Proper error handling** | Specific HTTP codes (401, 403, 404, 409, 422, 429) |
| **Soft delete** | Data preserved for audit trail |
| **Pagination** | Prevents loading entire database at once |
| **Rate limiting** | Prevents abuse |

**Architecture:**
```
User Request
     │
     ▼
[Validation] → Invalid? → Return 422
     │
     ▼
[Rate Check] → Exceeded? → Return 429
     │
     ▼
[Business Logic] → Blocked URL? → Return 409
     │                Password wrong? → Return 403
     │                Not found? → Return 404
     ▼
[Database] → Store/Retrieve
     │
     ▼
[Response] → Return proper HTTP code + JSON
```

---

### 3. Quality and Correctness of Generated Outputs

| Quality Metric | Evidence |
|----------------|----------|
| All code runs without errors | Server starts, all endpoints respond |
| All 26 tests pass | `python -m pytest tests/ -v` → 26 passed |
| Proper HTTP status codes | 201, 204, 302, 401, 403, 404, 409, 422, 429 |
| Input validation works | Bad URLs rejected, limits enforced |
| Security measures in place | Hashed passwords, parameterized SQL, rate limits |
| No dead code | Every function is used, every import is needed |
| Consistent patterns | All endpoints follow same structure |

---

### 4. Demonstrated Ownership of AI-Assisted Code

| How I Showed Ownership | Specific Example |
|------------------------|-----------------|
| **Caught AI bugs** | 6 mistakes found and fixed |
| **Rejected AI suggestions** | Said no to Redis, Docker, JWT, external libraries |
| **Made all design decisions** | Chose architecture, tech stack, features |
| **Added what AI missed** | Edge cases, security fixes, proper error messages |
| **Can explain every line** | Wrote DEMO_SCRIPT.md with business cases for each feature |
| **Understand limitations** | Documented what won't work at scale |

**The 6 AI Mistakes I Caught:**

| # | AI Did Wrong | I Fixed It |
|---|-------------|-----------|
| 1 | Deprecated startup pattern | Modern `lifespan` approach |
| 2 | Wrong route ordering (catch-all first) | Specific routes first |
| 3 | External library (install fails) | Built-in `random` module |
| 4 | Over-engineering (Redis, Docker) | Simple, portable approach |
| 5 | Plain text passwords | SHA-256 hashing |
| 6 | No rate limit cleanup | Auto-delete old records |

---

### 5. Validation Rigor and Testing Discipline

| Validation Layer | What It Catches |
|------------------|----------------|
| **Pydantic models** | Invalid input never reaches logic |
| **Automated tests (26)** | Regressions, broken features |
| **Manual Swagger testing** | End-to-end user experience |
| **Syntax checking** | Parse errors in all files |
| **Code review** | Logic errors, security issues |

**Test Discipline:**
```
Every feature has:
  ✓ Happy path test (it works)
  ✓ Error path test (it fails gracefully)
  ✓ Edge case test (boundary conditions)
```

| Feature | Happy Path | Error Path | Edge Case |
|---------|:----------:|:----------:|:---------:|
| Create URL | ✓ Valid URL works | ✓ Invalid rejects | ✓ Duplicate code |
| Click limit | ✓ Within limit | ✓ Over limit → 404 | ✓ Exactly at limit |
| Password | ✓ Correct → access | ✓ Wrong → 403 | ✓ No password → 401 |
| Expiration | ✓ Before expiry | ✓ After expiry → 404 | — |
| URL blocking | ✓ Safe URL works | ✓ Malicious → 409 | — |

---

### 6. Clarity and Defensibility of the Approach

| Question They Might Ask | My Answer |
|-------------------------|-----------|
| "Why SQLite?" | Zero setup, portable, perfect for demo. Production would use PostgreSQL. |
| "Why no authentication?" | Out of scope for demo. Documented as known limitation. Would add OAuth2 in production. |
| "Why static blocklist?" | Works offline, no API key needed. Production would use VirusTotal. |
| "Why FastAPI over Flask?" | Auto-generates interactive API docs — evaluators can test without writing code. |
| "How did AI help?" | Accelerated boilerplate (~40%). I made all decisions, caught 6 bugs, owned quality. |
| "What would you do differently at scale?" | PostgreSQL, Redis caching, API keys, Docker, CI/CD pipeline. |
| "What's the hardest part?" | Ambiguous requirement — "make it secure" meant nothing until I clarified it. |

---

## The Principle I Followed

> **"AI assists the engineer within tasks; the engineer owns execution and quality."**

| What This Means | How I Demonstrated It |
|-----------------|----------------------|
| AI assists | Used AI for code generation, test structure, doc drafts |
| Within tasks | AI worked on specific tasks I defined, not open-ended |
| Engineer owns execution | I decided architecture, features, trade-offs |
| Engineer owns quality | I caught 6 bugs, added edge cases, validated everything |

### Proof of Ownership (Not Just AI Output)

```
If AI built this alone, it would have:
  ✗ Used deprecated patterns (on_event)
  ✗ Wrong route ordering (broken API)
  ✗ External library (fails to install)
  ✗ Over-engineered (Redis + Docker + JWT)
  ✗ Plain text passwords (security vulnerability)
  ✗ No rate limit cleanup (database grows forever)

Because I reviewed and fixed everything:
  ✓ Modern patterns (lifespan)
  ✓ Correct route ordering
  ✓ Built-in modules only
  ✓ Simple, portable, demo-ready
  ✓ Hashed passwords
  ✓ Auto-cleanup of old records
```

---

## Summary — One Paragraph for Interview

> "I built a URL shortener service covering all three scenario types. For the greenfield scenario, I built the entire system from scratch — API, database, analytics. For brownfield, I added click limits, expiration, and password protection to the existing working system without breaking anything. For the ambiguous requirement 'make it secure,' I clarified what that means, then chose rate limiting and URL blocking. Throughout, I used AI to accelerate the repetitive coding work, but I made every design decision, caught 6 AI mistakes, wrote 26 tests, and can explain every line of code. The principle I followed: AI assists me within tasks, but I own execution and quality."
