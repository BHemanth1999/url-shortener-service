# Email Template — Assignment Submission

---

**Subject:** URL Shortener Service — Assessment Submission | Hemanth Kumar

---

Hi [Interviewer Name],

Thank you for the opportunity. Please find my assessment submission below.

**GitHub Repository:** https://github.com/hemanth67/url-shortener-service

---

## What I Built

A URL Shortener Service — a web application that converts long URLs into short, trackable links with access control, analytics, and security features.

**Tech Stack:** Python + FastAPI + SQLite (zero external setup needed)

---

## How to Run (3 steps)

```
1. pip install -r requirements.txt
2. python main.py
3. Open http://localhost:8000/docs (interactive API playground)
```

---

## Features Built (3 Groups)

| Group | Scenario | Features |
|-------|----------|----------|
| **CORE** | Greenfield (built from scratch) | Create, Redirect, Analytics, List, Delete |
| **ACCESS CONTROL** | Brownfield (added to existing) | Click limit, Expiration, Password, Bulk create |
| **SECURITY** | Ambiguous (clarified vague requirement) | Rate limiting, URL blocking |

---

## How AI Was Used

| AI Did | I (Engineer) Did |
|--------|-----------------|
| Generated boilerplate code (~40%) | Made all design decisions (100%) |
| Suggested approaches | Caught and fixed 6 AI mistakes |
| Drafted documentation | Verified accuracy, wrote real trade-offs |

---

## Assignment Requirements Coverage

| Requirement | How I Demonstrated It |
|-------------|----------------------|
| Effective AI usage | Used AI for repetitive code, made all decisions myself |
| Engineering ownership | Caught 6 AI mistakes, chose simpler approaches over AI suggestions |
| Rigorous validation | 26 automated tests + manual testing + syntax verification |
| Greenfield | Built entire URL shortener from zero |
| Brownfield | Added 4 features to working system without breaking it |
| Ambiguous requirements | Clarified "make it secure" → rate limiting + URL blocking |
| Test improvements | 26 automated tests covering all scenarios |
| Documentation improvements | 8 documents covering approach, decisions, AI usage, scenarios |

---

## Repository Structure (What's Inside)

```
hemanth/
├── main.py              ← Run this to start
├── app/                 ← Application code (4 files)
├── tests/               ← 26 automated tests
├── docs/                ← All documentation
│   ├── SUBMISSION_OVERVIEW.md  ← Start here
│   ├── HOW_I_BUILT_THIS.md    ← Detailed breakdown
│   ├── APPROACH.md             ← Problem-solving steps
│   ├── DECISIONS.md            ← Trade-offs made
│   ├── AI_USAGE.md             ← AI contribution details
│   └── SCENARIOS.md            ← All 3 scenarios with test commands
└── requirements.txt     ← Dependencies
```

**Recommended reading order:**
1. `docs/SUBMISSION_OVERVIEW.md` — maps requirements to files
2. `docs/HOW_I_BUILT_THIS.md` — detailed breakdown of approach
3. `README.md` — run the app and test features

---

I'm happy to walk through the code or demonstrate any feature during our discussion.

Best regards,
Hemanth Kumar
