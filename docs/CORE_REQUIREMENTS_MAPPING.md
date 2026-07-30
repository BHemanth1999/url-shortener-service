# Core Requirements — How I Addressed Each One

---

## 1. Requirement Understanding

### Original Requirement
> "Build a URL shortener service with APIs, persistence, and analytics"

### Ambiguities I Identified

| Ambiguity | Question I Asked | Decision Made |
|-----------|-----------------|---------------|
| What database? | SQL or NoSQL? Cloud or local? | SQLite — zero setup, portable |
| What analytics? | Just count? Or detailed? | Count + clicks by date + visitor info |
| "Scalable" means what? | Millions of users? Or demo? | Demo-ready, but designed for easy scaling |
| Security scope? | Auth? Encryption? Rate limit? | Rate limiting + URL blocking (practical) |
| Brownfield scenario? | What existing system to enhance? | Built core first, then added features to it |

### How I Converted It to an Engineering Problem

```
Vague: "URL shortener with APIs, persistence, analytics"

Clear:
├── REST API with 8 endpoints (CRUD + redirect + analytics)
├── SQLite database with 3 tables (urls, clicks, rate_limits)
├── Click tracking on every redirect
├── Input validation (reject bad URLs, enforce limits)
├── Access control (password, click limit, expiration)
└── Security (rate limiting, domain blocking)
```

---

## 2. Task Decomposition (Engineer-Led)

### Task Breakdown with Execution Sequence

| # | Task | Depends On | AI Assisted? | Time |
|:-:|------|:----------:|:------------:|:----:|
| 1 | Design database schema (3 tables) | — | Yes (generated SQL) | 10 min |
| 2 | Set up project structure | — | No (my decision) | 5 min |
| 3 | Build database layer (`database.py`) | Task 1 | Yes (boilerplate) | 10 min |
| 4 | Build validation models (`models.py`) | Task 1 | Yes (Pydantic) | 15 min |
| 5 | Build core service logic (`service.py`) | Task 3 | Yes (CRUD code) | 30 min |
| 6 | Build API routes (`routes.py`) | Task 4, 5 | Yes (endpoints) | 20 min |
| 7 | Add click limit feature | Task 5, 6 | Yes (logic) | 10 min |
| 8 | Add expiration feature | Task 5, 6 | Yes (datetime) | 10 min |
| 9 | Add password protection | Task 5, 6 | Yes (hashing) | 15 min |
| 10 | Add bulk creation | Task 5, 6 | Yes (loop) | 10 min |
| 11 | Add rate limiting | Task 3, 6 | Yes (counter) | 15 min |
| 12 | Add URL blocking | Task 5 | Partial (I chose approach) | 10 min |
| 13 | Write automated tests | Task 6-12 | Yes (structure) | 30 min |
| 14 | Write documentation | Task 6-12 | Yes (drafts) | 20 min |
| 15 | Validate and fix issues | Task 13 | No (all me) | 20 min |

### Dependency Diagram

```
Task 1 (DB schema)
  ├── Task 3 (database.py)
  │     └── Task 5 (service.py)
  │           ├── Task 7 (click limit)
  │           ├── Task 8 (expiration)
  │           ├── Task 9 (password)
  │           ├── Task 10 (bulk)
  │           ├── Task 11 (rate limit)
  │           └── Task 12 (URL block)
  └── Task 4 (models.py)
        └── Task 6 (routes.py)
              └── Task 13 (tests)
                    └── Task 15 (validate)
```

### How AI Assisted Within Each Task

| Task | My Role | AI's Role |
|------|---------|-----------|
| Database schema | Decided 3 tables, columns, relationships | Generated SQL CREATE statements |
| Service logic | Defined what each function does | Generated the function bodies |
| Routes | Decided endpoint structure and HTTP codes | Generated FastAPI decorator patterns |
| Tests | Decided what edge cases to test | Generated test boilerplate |
| Docs | Decided what to document | Drafted initial templates |

---

## 3. AI-Assisted Development

### Clear Prompting Examples

| What I Asked AI | What AI Gave Me | What I Changed |
|-----------------|-----------------|----------------|
| "Generate SQLite table for URLs with short_code, original_url, expiry" | CREATE TABLE with 10 columns | Removed 3 unnecessary columns, simplified |
| "Add rate limiting to FastAPI endpoint" | Redis-based solution | Replaced with simple SQLite counter (no Redis needed) |
| "Hash password for storage" | Used `bcrypt` library | Changed to built-in `hashlib.sha256` (no extra install) |
| "Write pytest for URL creation" | 3 basic tests | Expanded to 12 tests with edge cases |

### Iterative Refinement Example

**Round 1 — AI generated password storage:**
```python
# AI output — WRONG: stores plain text
conn.execute("INSERT INTO urls (..., password) VALUES (..., ?)", (password,))
```

**Round 2 — I identified the security risk:**
```python
# My fix — hash before storing
hashed = hashlib.sha256(password.encode()).hexdigest()
conn.execute("INSERT INTO urls (..., password) VALUES (..., ?)", (hashed,))
```

**Round 3 — I added verification on access:**
```python
# My addition — verify on redirect
if hash_password(input_password) != stored_hash:
    return "WRONG_PASSWORD"
```

### AI Suggestions I Rejected

| AI Suggested | I Rejected Because | I Chose Instead |
|--------------|-------------------|-----------------|
| Docker setup | Adds complexity for a demo | Direct `python main.py` |
| Redis for rate limiting | Extra service to install | SQLite table (already have it) |
| JWT authentication | Overkill for this scope | No auth (mentioned as limitation) |
| `shortuuid` library | Failed to install on some Python versions | Built-in `random` module |
| PostgreSQL | Requires separate installation | SQLite (zero setup) |

---

## 4. Engineering Output Generation

### Code Implementation

| File | Lines | Purpose | Quality Check |
|------|:-----:|---------|--------------|
| `main.py` | 15 | App entry point, modern lifespan pattern | Clean, minimal |
| `app/database.py` | 48 | Database setup, 3 tables | Proper connection handling |
| `app/models.py` | 105 | Input validation (Pydantic) | All fields validated |
| `app/service.py` | 270 | Business logic (all features) | Separated from routes |
| `app/routes.py` | 97 | API endpoints | Proper HTTP status codes |
| `tests/test_api.py` | ~300 | 26 automated tests | Isolated, comprehensive |

### API Contracts

| Endpoint | Method | Input | Output | Errors |
|----------|--------|-------|--------|--------|
| `/api/urls` | POST | URL + options | Short link | 409, 422, 429 |
| `/api/urls/bulk` | POST | List of URLs | Multiple links | 422, 429 |
| `/api/urls` | GET | page, limit | Paginated list | — |
| `/api/urls/{code}/analytics` | GET | short_code | Click stats | 404 |
| `/api/urls/{code}` | DELETE | short_code | 204 No Content | 404 |
| `/{code}` | GET | short_code | 302 Redirect | 401, 403, 404 |
| `/{code}/unlock` | POST | password | Original URL | 403, 404 |

### Database Schema

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `urls` | Stores all short links | short_code, original_url, max_clicks, expires_at, password, is_active |
| `clicks` | Records every click | url_id, clicked_at, ip_address, user_agent, referrer |
| `rate_limits` | Tracks requests per IP | ip_address, request_time |

### Design Principles Applied

| Principle | How I Applied It |
|-----------|-----------------|
| **Modularity** | 4 separate files, each with single responsibility |
| **Separation of concerns** | Routes → Service → Database (3-layer) |
| **Maintainability** | Clear function names, minimal dependencies |
| **Readability** | Simple Python, no complex patterns |
| **Correctness** | Input validation, proper error codes, edge case handling |

---

## 5. Validation and Quality Assurance

### Code Review Discipline

| What I Reviewed | What I Found | What I Fixed |
|-----------------|-------------|-------------|
| Route ordering | `/{code}` before `/api/*` | Reordered (specific routes first) |
| Password handling | Plain text storage | SHA-256 hashing |
| Startup pattern | Deprecated `on_event` | Modern `lifespan` context manager |
| Redirect type | 301 (browser caches) | 302 (server always hit) |
| Dependencies | `shortuuid` install fails | Built-in `random` module |
| Rate limit cleanup | Old records never deleted | Added DELETE for expired records |

### Test Coverage

| Feature | # Tests | What's Tested |
|---------|:-------:|---------------|
| Create URL | 3 | Valid, invalid URL, duplicate code |
| Redirect | 2 | Success, not found |
| Analytics | 1 | Click count accuracy |
| List URLs | 1 | Pagination |
| Delete | 2 | Success, not found |
| Click limit | 4 | Works within limit, blocks after limit |
| Expiration | 2 | Works before expiry, blocks after |
| Password | 5 | No password, wrong password, correct password |
| Bulk create | 2 | Multiple URLs, invalid URL in batch |
| Rate limiting | 1 | Blocks after 10 requests |
| URL blocking | 2 | Blocks malicious, allows safe |
| **Total** | **26** | **All pass** |

### Security Awareness

| Risk | How I Addressed It |
|------|-------------------|
| SQL Injection | Parameterized queries (`?` placeholders) everywhere |
| Plain text passwords | SHA-256 hashing |
| Spam/abuse | Rate limiting (10 req/min per IP) |
| Malicious URLs | Domain blocklist |
| Data loss on delete | Soft delete (is_active flag) |
| Invalid input | Pydantic validation on all endpoints |

### Performance Awareness

| Consideration | How I Addressed It |
|---------------|-------------------|
| Database grows forever | Rate limit records auto-cleaned |
| Large result sets | Pagination (limit 10 per page, max 100) |
| Bulk operations | Capped at 50 URLs per batch |

---

## 6. Risk Awareness

### Functional Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| SQLite doesn't scale to millions | Not suitable for production at scale | Documented as limitation; can swap to PostgreSQL |
| Static blocklist gets outdated | New malicious domains not caught | Document as known limitation; can integrate external API |
| No authentication | Anyone can create/delete URLs | Documented as trade-off for demo simplicity |
| Rate limit per IP only | VPN users bypass it | Acceptable for demo; production would add API keys |

### AI-Related Risks

| Risk | Example | How I Mitigated |
|------|---------|-----------------|
| Incorrect code | AI stored passwords as plain text | Manually reviewed every security-related function |
| Coverage gaps | AI tests missed edge cases | Added 10+ edge case tests manually |
| Over-engineering | AI suggested Redis, Docker, JWT | Rejected unnecessary complexity |
| Deprecated patterns | AI used `on_event` (deprecated) | Researched current best practices |
| Dependency risks | AI suggested library that fails to install | Used built-in alternatives |

### Trade-offs Made

| Decision | Pro | Con | Why I Chose It |
|----------|-----|-----|---------------|
| SQLite over PostgreSQL | Zero setup | Not scalable | Demo-friendly, portable |
| No authentication | Easy to use and demo | Anyone can access | Scope limitation, documented |
| Static blocklist | No external API needed | Gets outdated | Simple, works offline |
| SHA-256 over bcrypt | No extra library | Less secure than bcrypt | Acceptable for demo scope |
| Soft delete | Audit trail kept | DB grows | Compliance benefit outweighs |

---

## 7. Final Engineering Summary

### Implementation Approach and Rationale

| Decision | Rationale |
|----------|-----------|
| Python + FastAPI | Simple, readable, auto-generates interactive API docs |
| SQLite | Zero setup, single file, works on any machine |
| 3-layer architecture | Separation of concerns, easy to test and modify |
| No external services | Portable — runs anywhere with Python installed |
| Incremental development | Built core first, then added features one by one |

### Generated Artifacts

| Type | Artifact | Location |
|------|----------|----------|
| Code | 5 Python files (app + entry point) | `main.py`, `app/` |
| Tests | 26 automated tests | `tests/test_api.py` |
| API | 8 REST endpoints + OpenAPI spec | `app/routes.py` + `/docs` |
| Database | SQLite with 3 tables | Auto-created `data/urls.db` |
| Documentation | 8 markdown documents | `docs/` |

### Risks and Validation Approach

| Risk Category | How Validated |
|---------------|--------------|
| Correctness | 26 automated tests, all passing |
| Security | Parameterized queries, hashed passwords, input validation |
| AI errors | Manual code review, caught 6 issues |
| Compatibility | Tested on Python 3.13, no version-pinned deps |

### Assumptions

| Assumption | Impact If Wrong |
|------------|----------------|
| Single user demo (not production scale) | Would need PostgreSQL + caching for scale |
| No authentication needed for demo | Production would need API keys/OAuth |
| Blocked domains are static list | Production would use real-time threat API |
| Running locally (localhost) | Production would need domain + HTTPS |

### Limitations (Known and Documented)

| Limitation | Why It's Acceptable | Production Fix |
|------------|-------------------|----------------|
| SQLite (single file) | Demo doesn't need scale | PostgreSQL |
| No auth | Demo simplicity | OAuth2 / API keys |
| Static blocklist | Works offline | VirusTotal API |
| IP-based rate limit | Simple but bypassable | Token-based + Redis |
| No HTTPS | Localhost only | Nginx + SSL cert |
