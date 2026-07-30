# Submission Overview

## What I Built

A **URL Shortener Service** — a web application that converts long URLs into short, trackable links with access control and analytics.

---

## Assignment Requirements → Where to Find Them

| # | Assignment Requirement | Where It's Covered |
|---|---|---|
| 1 | Requirement Understanding | [docs/APPROACH.md](APPROACH.md) → Step 1 |
| 2 | Task Decomposition (Engineer-Led) | [docs/APPROACH.md](APPROACH.md) → Step 2 (task table with sequence) |
| 3 | AI-Assisted Development | [docs/AI_USAGE.md](AI_USAGE.md) → Full breakdown of AI usage per task |
| 4 | Engineering Output (code, APIs, tests, docs) | Source code in `app/`, tests in `tests/`, docs in `docs/` |

---

## Deliverables → Where to Find Them

| # | Deliverable | Location |
|---|---|---|
| 1 | Working Prototype | Run `python main.py` → open `http://localhost:8000/docs` |
| 2 | Architecture Overview | [docs/APPROACH.md](APPROACH.md) → Step 3 + diagram below |
| 3 | Example Scenarios (Greenfield, Brownfield, Ambiguous) | [docs/SCENARIOS.md](SCENARIOS.md) |
| 4 | Setup Instructions | [README.md](../README.md) → Setup & Run section |
| 5 | Testing Approach | 26 automated tests in `tests/test_api.py` + run with `pytest tests/ -v` |

---

## Tech Stack

| What | Technology | Why I Chose It |
|------|-----------|----------------|
| Programming Language | Python | Simple, readable, widely used |
| Web Framework | FastAPI | Automatically generates interactive API documentation |
| Database | SQLite | Zero setup needed — just a file, works anywhere |
| Testing | Pytest | Industry standard for Python testing |
| Validation | Pydantic | Automatically rejects bad input |

---

## Architecture (How the App is Structured)

```
┌─────────────────────────────────────────────────┐
│              USER (Browser / Swagger UI)          │
└────────────────────────┬────────────────────────┘
                         │ clicks / sends request
                         ▼
┌─────────────────────────────────────────────────┐
│              ROUTES (routes.py)                   │
│         "The receptionist"                       │
│   - Receives requests from user                  │
│   - Sends back responses                         │
│   - Checks rate limits                           │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│              SERVICE (service.py)                 │
│         "The brain"                              │
│   - Creates short codes                          │
│   - Checks passwords, click limits, expiry       │
│   - Records analytics                            │
│   - Blocks malicious URLs                        │
└────────────────────────┬────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────┐
│              DATABASE (database.py + SQLite)      │
│         "The filing cabinet"                     │
│   - urls table (all short links)                 │
│   - clicks table (every visit recorded)          │
│   - rate_limits table (spam prevention)          │
└─────────────────────────────────────────────────┘
```

---

## Features Built

| # | Feature | Business Purpose | Scenario Type |
|---|---------|-----------------|---------------|
| 1 | Create short URL | Clean links for emails/SMS | Greenfield |
| 2 | Custom short codes | Branded links (e.g. /invest2026) | Greenfield |
| 3 | Redirect | Click short link → go to original | Greenfield |
| 4 | Click analytics | Track who clicked, when, from where | Greenfield |
| 5 | List all URLs | Admin view of all links | Greenfield |
| 6 | Delete URL | Remove access (soft delete for audit) | Greenfield |
| 7 | Click limit | Link dies after N clicks (controlled distribution) | Brownfield |
| 8 | Expiration | Link dies after X hours (time-limited offers) | Brownfield |
| 9 | Password protection | Only password-holders can access | Brownfield |
| 10 | Bulk creation | Create 50 links at once (campaigns) | Brownfield |
| 11 | Rate limiting | Block spammers (max 10 requests/min) | Ambiguous (Security) |
| 12 | URL blocking | Reject malicious/phishing domains | Ambiguous (Security) |

---

## Folder Structure

```
hemanth/
│
├── main.py                  ← START HERE (run this to start the app)
│
├── app/                     ← APPLICATION CODE
│   ├── database.py          ← Database setup (creates tables)
│   ├── models.py            ← Input validation rules
│   ├── service.py           ← All business logic (the brain)
│   └── routes.py            ← API endpoints (the door)
│
├── tests/                   ← AUTOMATED TESTS
│   └── test_api.py          ← 26 tests covering all features
│
├── docs/                    ← DOCUMENTATION
│   ├── SUBMISSION_OVERVIEW.md  ← THIS FILE (start reading here)
│   ├── APPROACH.md          ← How I broke down the problem
│   ├── AI_USAGE.md          ← How AI tools helped (and what I fixed)
│   └── SCENARIOS.md         ← 3 scenario examples with test instructions
│
├── requirements.txt         ← List of packages to install
└── README.md                ← Quick start guide
```

---

## How to Run

```
Step 1:  pip install -r requirements.txt    (install packages — one time)
Step 2:  python main.py                     (start the server)
Step 3:  Open browser → http://localhost:8000/docs   (interactive UI)
Step 4:  pytest tests/ -v                   (run all 26 tests)
```

---

## Summary

- **Language:** Python
- **Features:** 12 features covering all 3 scenario types
- **Tests:** 26 automated tests, all passing
- **Architecture:** 3-layer (Routes → Service → Database)

---

## Reading Order

1. **Run the app** → Follow README.md setup steps
2. **See the process** → docs/APPROACH.md
3. **See AI usage** → docs/AI_USAGE.md
