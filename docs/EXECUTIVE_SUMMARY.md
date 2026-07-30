# URL Shortener — What I Built & Why

---

## The Problem

Long URLs like `https://www.example.com/campaigns/2026/summer-sale?utm_source=email&ref=abc123` are ugly, hard to share, and impossible to track.

**Solution:** A service that converts long URLs into short, trackable links — like Bitly, but built from scratch.

---

## What It Does (Simple Version)

| You Give It | It Returns | Example |
|-------------|-----------|---------|
| A long URL | A short link | `localhost:8000/sale26` |
| A short link click | Redirect to original | User lands on the real page |
| Nothing (just ask) | Click analytics | "42 people clicked, mostly on Monday" |

---

## How I Approached the Assignment

| Step | What I Did |
|------|-----------|
| 1 | Read the requirements, identified 3 scenario types |
| 2 | Broke the problem into small tasks (engineer-led) |
| 3 | Used AI to speed up repetitive coding, reviewed everything |
| 4 | Built features incrementally, tested each one |
| 5 | Documented decisions, trade-offs, and AI usage |

---

## What Was Built

| Group | What | Real-World Use Case |
|-------|------|-------------------|
| **Core** | Create, redirect, track clicks | Marketing team shares clean links in emails |
| **Access Control** | Click limits, expiration, passwords | "Only first 50 people get access" or "Link expires Friday" |
| **Security** | Rate limiting, URL blocking | Prevents spam bots and phishing links |

---

## How the 3 Scenarios Map

| Scenario | Meaning | My Example |
|----------|---------|-----------|
| **Greenfield** | Build something brand new | Built the entire URL shortener from zero |
| **Brownfield** | Add features to existing code | Added click limits, expiration, passwords to the working app |
| **Ambiguous** | Requirement is vague — you clarify it | "Make it secure" → I decided: rate limiting + URL blocking |

---

## How AI Was Used

| AI Did | I (Engineer) Did |
|--------|-----------------|
| Generated boilerplate code | Made all design decisions |
| Suggested structures | Caught and fixed 6 AI mistakes |
| Drafted docs | Verified accuracy, added real trade-offs |

**Key point:** AI assisted ~40% of the typing. Engineer owned 100% of the decisions and quality.

---

## Tech Choices (and Why)

| Choice | Reason |
|--------|--------|
| Python | Simple, readable, widely known |
| FastAPI | Automatically generates interactive API documentation |
| SQLite | Zero setup — just one file, works on any machine |
| No Docker/Redis/Cloud | Keeps it portable — runs anywhere with Python installed |

---

## How to Run It

```
1. pip install -r requirements.txt    (one-time setup)
2. python main.py                     (starts the app)
3. Open browser → http://localhost:8000/docs   (try it live)
```

That's it. No Docker, no cloud setup, no database installation needed.

---

## How to Verify It Works

- **Automated tests:** `pytest tests/ -v` → 26 tests, all pass
- **Manual testing:** Swagger UI at `/docs` lets you click and try every feature
- **Live demo:** Create a link, click it, check analytics — all in browser

---

## What's Included in the Submission

| Item | File/Folder |
|------|------------|
| Working application | `main.py` + `app/` folder |
| 26 automated tests | `tests/test_api.py` |
| Architecture overview | `docs/SUBMISSION_OVERVIEW.md` |
| Problem approach | `docs/APPROACH.md` |
| Decisions & trade-offs | `docs/DECISIONS.md` |
| AI usage documentation | `docs/AI_USAGE.md` |
| All 3 scenarios with examples | `docs/SCENARIOS.md` |
| Full API reference | `docs/API_CONTRACT.md` |

---

## Summary in 3 Lines

1. Built a complete URL shortener covering all 3 scenario types (greenfield, brownfield, ambiguous)
2. AI accelerated development; engineer owned all decisions and caught 6 AI mistakes
3. Fully testable, portable, documented — runs with one command on any machine with Python
