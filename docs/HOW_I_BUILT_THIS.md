# How I Built This Project

---

## 1. Effective Use of AI Tools Across Development Tasks

| Task | What AI Did | What I Did (Engineer) |
|------|-------------|----------------------|
| Project setup | Suggested folder structure | Chose 3-layer architecture (routes → service → database) |
| Database design | Generated SQL table schema | Simplified it, removed unnecessary columns |
| CRUD endpoints | Generated boilerplate code | Fixed error handling, added proper HTTP status codes |
| Click limit feature | Generated check logic | Ensured it works with existing URLs (backwards compatible) |
| Expiration feature | Generated datetime logic | Verified timezone handling, added seconds support |
| Password protection | Suggested basic approach | Caught plain-text mistake, added SHA-256 hashing |
| Bulk creation | Generated loop logic | Added per-URL error handling (one bad URL doesn't fail all) |
| Rate limiting | Generated counter logic | Decided 10 requests/60 seconds window |
| URL blocking | Suggested external API approach | Chose simpler static blocklist (no dependency) |
| Tests | Generated test structure | Added edge cases, expanded to 26 tests |
| Documentation | Drafted templates | Ensured accuracy, wrote real trade-offs |

**Result:** AI accelerated ~40% of typing. I made 100% of design decisions.

---

## 2. Strong Engineering Ownership of All Outputs

### Decisions I Made (Not AI)

| Decision | Why I Chose This | What AI Suggested Instead |
|----------|-----------------|--------------------------|
| SQLite over PostgreSQL | Zero setup, portable, demo-friendly | PostgreSQL (overkill for demo) |
| FastAPI over Flask | Auto-generates interactive API docs | Flask (no auto docs) |
| Built-in `random` over external library | No extra dependency, avoids install issues | `shortuuid` library (failed to install) |
| SHA-256 over plain text passwords | Security best practice | Initially stored plain text |
| Static blocklist over external API | No API key needed, works offline | External malware-check API |
| Soft delete over hard delete | Keeps audit trail for compliance | Hard delete (data lost forever) |
| 302 redirect over 301 | Browser doesn't cache, click limit works properly | 301 (browser caches, bypasses server) |

### AI Mistakes I Caught and Fixed

| # | AI Mistake | Risk If I Didn't Catch It | My Fix |
|---|-----------|---------------------------|--------|
| 1 | Used deprecated `on_event("startup")` | Console warnings in production | Replaced with modern `lifespan` pattern |
| 2 | Put `/{code}` route before `/api/*` routes | All API endpoints unreachable | Reordered routes (specific before generic) |
| 3 | Suggested `shortuuid` external library | Install fails on some Python versions | Used built-in `random` module |
| 4 | Over-engineered (Redis, Docker, JWT) | Too complex to demo, too many dependencies | Scoped to essentials only |
| 5 | Stored password as plain text | Security vulnerability | Added SHA-256 hashing |
| 6 | No cleanup of rate limit records | Database grows forever | Added DELETE for old entries |

**Key Point:** I didn't blindly accept AI output. Every line was reviewed, tested, and validated.

---

## 3. Rigorous Validation of AI-Generated Results

| Validation Method | What It Checks | Result |
|-------------------|---------------|--------|
| `py_compile` on all files | Syntax errors | All 6 files pass |
| 26 automated tests | Logic correctness | All pass |
| Parameterized SQL queries | SQL injection prevention | Safe |
| Pydantic validators | Input validation (bad URLs, invalid formats) | Rejects bad input |
| SHA-256 password hashing | Never stores plain text | Verified |
| Manual Swagger UI testing | End-to-end feature correctness | All 12 features work |
| Edge case testing | Click limit=0, expired links, wrong passwords | All handled |

### Validation Process I Followed

```
For every AI-generated code:
  1. Read it — do I understand every line?
  2. Question it — could this fail? What edge cases?
  3. Test it — does it actually work with real inputs?
  4. Fix it — if wrong, fix and document why
```

---

## 4. Scope Coverage

### Greenfield — New System Development

| What I Built From Scratch | Business Purpose |
|---------------------------|-----------------|
| Short URL creation (auto + custom codes) | Clean links for emails/SMS |
| Redirect with tracking | Users click short link → go to original |
| Click analytics (count, dates, visitors) | "How many people clicked our campaign?" |
| List all URLs (paginated) | Admin dashboard view |
| Soft delete | Remove links but keep audit trail |

**How:** Started with empty project → designed database → built API layer → added tests.

---

### Brownfield — Enhancements to Existing System

| What I Added to the Working App | Business Purpose |
|---------------------------------|-----------------|
| Click limit (max N clicks) | "Only first 50 customers get the discount" |
| Expiration (auto-deactivate) | "Flash sale link dies after 24 hours" |
| Password protection | "Only my team can access this document" |
| Bulk creation (up to 50 at once) | "Marketing needs 50 campaign links now" |

**How:** App was already working → added features without breaking existing functionality → tested both old and new features together.

---

### Ambiguous Requirement — "Make It More Secure"

| Step | What I Did |
|------|-----------|
| 1. Received vague requirement | "The URL shortener needs to be more secure" |
| 2. Asked clarifying questions | "Secure from what? What kind of abuse?" |
| 3. Identified two real threats | Spam bots + phishing/malware links |
| 4. Chose practical solutions | Rate limiting (10 req/min) + URL domain blocking |
| 5. Documented trade-offs | Simple but effective; acknowledged limitations |

**Key Point:** Didn't guess or over-engineer. Clarified → decided → built → documented why.

---

### Test Improvements

| What | Details |
|------|---------|
| 26 automated tests | Covers all 12 features |
| Edge cases covered | Expired links, wrong passwords, duplicate codes, blocked URLs |
| Test isolation | Each test gets fresh database (no interference) |
| Easy to run | Single command: `python -m pytest tests/ -v` |

---

### Documentation Improvements

| Document | Purpose |
|----------|---------|
| README.md | Quick start + feature overview |
| SUBMISSION_OVERVIEW.md | Maps every assignment requirement to files |
| APPROACH.md | Step-by-step problem breakdown |
| DECISIONS.md | Trade-offs and assumptions |
| AI_USAGE.md | AI contribution + mistakes caught |
| SCENARIOS.md | All 3 scenarios with test commands |
| API_CONTRACT.md | Full API reference |
| DEMO_SCRIPT.md | Business cases for each feature |

---

## Summary

| Requirement | How I Demonstrated It |
|-------------|----------------------|
| Effective AI usage | Used AI for boilerplate, made all decisions myself |
| Engineering ownership | Caught 6 AI mistakes, chose simpler approaches |
| Rigorous validation | 26 tests + manual testing + syntax checks |
| Greenfield | Built entire URL shortener from zero |
| Brownfield | Added 4 features to working system without breaking it |
| Ambiguous requirements | Clarified "make it secure" → rate limiting + URL blocking |
| Test improvements | 26 automated tests covering all scenarios |
| Documentation improvements | 8 documents explaining everything |
