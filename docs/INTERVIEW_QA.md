# Interview Questions & Answers — Cheat Sheet

---

## About the Project

### Q: Walk me through what you built.
> "I built a URL shortener — like Bitly — that converts long URLs into short trackable links. It has 12 features covering 3 scenario types: greenfield (built from scratch), brownfield (added features to existing system), and ambiguous (clarified a vague requirement). It runs with one command, has 26 automated tests, and interactive API docs."

### Q: Why did you choose this tech stack?
> "Python because it's simple and readable. FastAPI because it auto-generates interactive API documentation — so you can test everything without writing code. SQLite because it needs zero setup — just run and it works. No Docker, no database installation, nothing extra."

### Q: How long did it take?
> "The core system took about 3-4 hours. Documentation and testing added another 2 hours. AI accelerated the boilerplate by about 40%, but all design decisions and validation were mine."

### Q: Can this scale to millions of users?
> "As built — no. SQLite is single-file, single-writer. For production scale, I'd swap to PostgreSQL for the database, add Redis for caching frequently accessed URLs, put it behind a load balancer, and add API key authentication. The 3-layer architecture makes this swap easy — only database.py changes."

---

## About AI Usage

### Q: How did you use AI in this project?
> "I used AI like a junior developer on my team. I told it WHAT to build, it wrote the first draft, I reviewed it, fixed issues, and approved the final code. AI handled about 40% of the typing — boilerplate, repetitive patterns. I made 100% of the design decisions and caught 6 AI mistakes."

### Q: What mistakes did AI make?
> "Six that I caught:
> 1. Used deprecated startup pattern — I replaced with modern approach
> 2. Wrong route ordering — API endpoints were unreachable
> 3. Suggested external library that fails to install — I used built-in module
> 4. Over-engineered with Redis and Docker — I kept it simple
> 5. Stored passwords as plain text — I added SHA-256 hashing
> 6. No cleanup of rate limit records — I added auto-deletion"

### Q: How do you validate AI-generated code?
> "Four steps: First, I read every line — do I understand it? Second, I question it — what could go wrong? Third, I test it — automated tests plus manual testing. Fourth, I fix anything wrong and document why. I never accept AI output without review."

### Q: What AI suggestions did you reject and why?
> "I rejected Redis (extra service to install for a demo), Docker (adds complexity), JWT authentication (overkill for scope), shortuuid library (failed to install), and PostgreSQL (requires separate setup). In each case, I chose the simpler option that still demonstrates the concept."

### Q: How is this different from just letting AI build everything?
> "If AI built this alone, it would have deprecated patterns, wrong route ordering, a library that doesn't install, over-engineering, and plain text passwords. Because I reviewed everything, I caught and fixed 6 issues. The final code is simpler, more secure, and actually works on any machine."

---

## About Architecture & Design

### Q: Explain your architecture.
> "Three layers — like a restaurant. Routes is the waiter (takes orders, delivers food). Service is the kitchen (does the actual cooking). Database is the pantry (stores ingredients). Each layer has one job, can be tested independently, and can be swapped without affecting others."

### Q: Why 3-layer architecture?
> "Separation of concerns. If I need to switch from SQLite to PostgreSQL, I only change database.py. If I need to add a new endpoint, I only touch routes.py. Nothing else breaks. It's also easier to test — I can test business logic without starting the server."

### Q: Why SQLite over PostgreSQL?
> "For this demo: zero setup. You just run `python main.py` and it works. No database installation, no Docker, no configuration. For production, I'd switch to PostgreSQL — and thanks to the layered architecture, only one file changes."

### Q: Why soft delete instead of hard delete?
> "Audit trail. In a real company, if someone asks 'who deleted that campaign link?', we need records. Soft delete marks it as inactive but keeps the data. It's also reversible — we can undelete if it was a mistake."

### Q: Why 302 redirect instead of 301?
> "301 means 'permanent' — browsers cache it and never ask the server again. That breaks our click tracking and click limit features. 302 means 'temporary' — browser always asks the server, so we can count clicks and enforce limits."

---

## About Specific Features

### Q: How does rate limiting work?
> "Every request, we record the IP address and time. Before processing a new request, we count how many requests that IP made in the last 60 seconds. If it's 10 or more, we reject with 429. Old records are auto-deleted to prevent database growth."

### Q: How does password protection work?
> "When creating a URL with a password, we hash it with SHA-256 before storing (never plain text). On access, we hash the provided password and compare hashes. No match = 403 forbidden. No password provided = 401 unauthorized."

### Q: How does URL blocking work?
> "We maintain a blocklist of known malicious domains. Before creating any short URL, we extract the domain from the URL and check against the list. If it matches, we reject with 409. This prevents our platform from being used to spread phishing links."

### Q: How does click limit work?
> "When a URL has max_clicks set, every redirect request first counts existing clicks. If count >= max_clicks, we return 404 instead of redirecting. The analytics endpoint shows remaining clicks so users know how many are left."

### Q: How does expiration work?
> "When creating a URL with expires_in_hours or expires_in_seconds, we calculate the future timestamp and store it. On every redirect request, we compare current time with expires_at. If expired, return 404."

---

## About Testing

### Q: How did you test this?
> "Three levels: 1) Syntax checking — all files compile without errors. 2) Automated tests — 26 tests covering all features, edge cases, error paths. 3) Manual testing — used Swagger UI to test every endpoint end-to-end. Tests run in isolation — each test gets a fresh database."

### Q: What edge cases did you test?
> "Expired URLs, wrong passwords, click limits reached, duplicate short codes, invalid URL formats, blocked domains, rate limit exceeded, bulk creation with one invalid URL in the batch, accessing deleted URLs. Every feature has a happy path test AND an error path test."

### Q: How do you ensure tests don't interfere with each other?
> "Each test function gets a fresh database using a pytest fixture with `autouse=True`. The database is created before each test and cleaned up after. So test order doesn't matter and they can run in parallel."

---

## About Scenarios

### Q: Explain the greenfield scenario.
> "Started with zero code. Designed the database, built the API layer, added redirect and analytics. This demonstrates building a new system from scratch — like a startup's first feature."

### Q: Explain the brownfield scenario.
> "After the core was working, I added click limits, expiration, password protection, and bulk creation. The key challenge: don't break existing features. All original tests still pass after adding new features. This demonstrates real-world feature development on a live system."

### Q: Explain the ambiguous scenario.
> "The requirement was 'make it more secure.' That could mean 20 different things. I clarified: 'Secure from what?' Answer: spam bots and malicious links. Then I chose two practical solutions: rate limiting (blocks bots) and URL blocking (prevents phishing). This demonstrates how engineers handle vague requirements — clarify first, then build."

---

## About Trade-offs & Risks

### Q: What are the limitations?
> "Five main ones: SQLite doesn't scale to millions, no authentication (anyone can create/delete), static blocklist gets outdated, rate limit bypassed with VPN, no HTTPS. All are documented and all have clear production fixes."

### Q: What would you change for production?
> "Five things: 1) PostgreSQL for the database. 2) Redis for caching hot URLs. 3) OAuth2/API keys for authentication. 4) External threat API for URL blocking. 5) Docker + CI/CD for deployment. The 3-layer architecture makes each swap straightforward."

### Q: What risks did you identify?
> "Two types. Functional risks: SQLite won't handle concurrent writes at scale, static blocklist gets outdated. AI risks: AI generated deprecated code, wrong route ordering, plain text passwords, unnecessary dependencies. I mitigated AI risks by reviewing every line and testing thoroughly."

---

## Tricky Questions

### Q: Did AI write this entire project?
> "AI assisted with about 40% of the code generation — the repetitive, boilerplate parts. But I made every architectural decision, caught 6 AI bugs, wrote edge case tests, chose the tech stack, and can explain every line. If I just accepted AI output, the app would have security vulnerabilities and broken features."

### Q: What's the most interesting technical decision you made?
> "Changing from 301 to 302 redirect. AI suggested 301 (permanent redirect). But 301 means the browser caches it forever and never asks our server again — which completely breaks click tracking and click limits. Switching to 302 (temporary) fixed this. It's a subtle decision that shows understanding of HTTP semantics beyond just 'it works.'"

### Q: If you had more time, what would you add?
> "Custom analytics dashboard (frontend), user authentication, QR code generation for each short URL, URL preview (show where it goes before clicking), and a Chrome extension for one-click shortening. But I kept scope focused on demonstrating the three scenario types clearly."

### Q: How do you ensure this is production-grade?
> "For a demo, it hits the production-grade bar in: code structure (modular, testable), error handling (proper HTTP codes, validation), security (hashed passwords, parameterized SQL, rate limiting), and testing (26 automated tests). What's missing for true production: authentication, HTTPS, scaled database, monitoring, and CI/CD."

---

## One-Liner Answers (Quick Reference)

| Question | One-Line Answer |
|----------|----------------|
| What is this? | URL shortener like Bitly with security and analytics |
| Tech stack? | Python + FastAPI + SQLite |
| How to run? | `pip install -r requirements.txt` then `python main.py` |
| How many features? | 12 features in 3 groups (Core, Access Control, Security) |
| How many tests? | 26 automated tests, all pass |
| How AI helped? | 40% code generation, 100% decisions were mine |
| AI mistakes? | Caught and fixed 6 |
| Why SQLite? | Zero setup, works anywhere |
| Why FastAPI? | Auto-generates interactive API docs |
| Scalable? | Architecture yes, database no — swap SQLite for PostgreSQL |
| Production ready? | Demo-grade yes, needs auth + HTTPS + scaled DB for production |
