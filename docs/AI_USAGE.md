# How AI Tools Were Used in this Project


## Where AI Helped

| Task | AI did | What i Enhanced |
|------|--------|-------------|
| Project structure | Suggested folder layout | Chose 3-layer pattern |
| Database schema | Generated SQL for 3 tables | Simplified, added indexes |
| Click limit | Generated check logic | Ensured backwards compatibility |
| Expiration | Generated datetime logic | Verified timezone handling |
| Password protection | Suggested hashing approach | Chose SHA-256, validated security |
| Rate limiting | Generated counter logic | Decided window size (60s) and limit (10) |
| Tests | Generated test structure | Added edge cases (26 total) |

---

## AI Mistakes I Caught and Fixed

| # | AI Mistake | Risk | My Fix |
|---|-----------|------|--------|
| 1 | Used deprecated `on_event("startup")` | Console warnings | Replaced with `lifespan` |
| 2 | Route ordering: `/{code}` before `/api/*` | API endpoints unreachable | Reordered routes |
| 3 | Stored password in plain text initially | Security vulnerability | Added SHA-256 hashing |
| 4 | No rate limit cleanup | Table grows forever | Added DELETE for old entries |

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
- Added some extra features
- I have caught 6 issues that AI introduced
