# How AI Tools Were Used

## Principle

> "AI assists the engineer within tasks; the engineer owns execution and quality."

---

## Where AI Helped

| Task | AI did | Engineer did |
|------|--------|-------------|
| Project structure | Suggested folder layout | Chose 3-layer pattern |
| Database schema | Generated SQL for 3 tables | Simplified, added indexes |
| CRUD code | Generated boilerplate | Fixed error handling, added edge cases |
| Click limit | Generated check logic | Ensured backwards compatibility |
| Expiration | Generated datetime logic | Verified timezone handling |
| Password protection | Suggested hashing approach | Chose SHA-256, validated security |
| Bulk endpoint | Generated loop logic | Added error handling per-URL |
| Rate limiting | Generated counter logic | Decided window size (60s) and limit (10) |
| URL blocking | Suggested blocklist approach | Decided to keep it simple (static list) |
| Tests | Generated test structure | Added edge cases (26 total) |
| Documentation | Drafted templates | Ensured accuracy, added real trade-offs |

---

## AI Mistakes I Caught and Fixed

| # | AI Mistake | Risk | My Fix |
|---|-----------|------|--------|
| 1 | Used deprecated `on_event("startup")` | Console warnings | Replaced with `lifespan` |
| 2 | Route ordering: `/{code}` before `/api/*` | API endpoints unreachable | Reordered routes |
| 3 | Suggested external library for short codes | Extra dependency, install issues | Used built-in `random` |
| 4 | Over-engineered (Redis, Docker, JWT) | Too complex for demo | Scoped to essentials |
| 5 | Stored password in plain text initially | Security vulnerability | Added SHA-256 hashing |
| 6 | No rate limit cleanup | Table grows forever | Added DELETE for old entries |

---

## Example: Iterative Refinement

### Version 1 (AI-generated):
```python
# AI suggested - stores password as plain text!
conn.execute("INSERT INTO urls (..., password) VALUES (..., ?)", (password,))
```

### Version 2 (Engineer-fixed):
```python
# Engineer added hashing - never store plain text passwords
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()
conn.execute("INSERT INTO urls (..., password) VALUES (..., ?)", (hashed,))
```

### Version 3 (Engineer-validated):
```python
# Also verify password on access
if hash_password(input_password) != stored_hash:
    return "WRONG_PASSWORD"
```

---

## Validation Checklist

| Check | Method | Result |
|-------|--------|--------|
| Syntax | `py_compile` all files | All pass |
| Logic | 26 automated tests | All pass |
| SQL injection | Parameterized queries (`?`) | Safe |
| Password security | SHA-256 hashing | Never plain text |
| Input validation | Pydantic validators | Bad input rejected |
| Error codes | Correct HTTP status codes | 201, 401, 403, 404, 409, 422, 429 |
| Edge cases | Click limit, expiration, wrong password | All handled |

---

## Summary

- AI accelerated development by ~3x for boilerplate tasks
- Engineer caught 6 issues that AI introduced
- All design decisions were engineer-led
- Every line of code was reviewed and validated before acceptance
