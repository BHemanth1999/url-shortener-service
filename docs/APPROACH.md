# Approach: How I Built This

## Requirement

> "Build a scalable URL shortener service with APIs, persistence, and analytics."

## Step 1: Breaking Down the Requirement

| Feature | Priority | Why |
|---------|----------|-----|
| Shorten a URL | Must have | Core functionality |
| Redirect with tracking | Must have | Core + analytics |
| Click analytics | Must have | Explicitly requested |
| Click limit | Should have | Controlled distribution (brownfield) |
| URL expiration | Should have | Time-limited links (brownfield) |
| Password protection | Should have | Secure document sharing (brownfield) |
| Bulk creation | Nice to have | Marketing team efficiency |
| Rate limiting | Must have | Prevent abuse (security) |
| URL blocking | Must have | Prevent malicious links (security) |

## Step 2: Implementation Tasks

| # | Task | Dependency |
|---|------|------------|
| 1 | Setup project structure | None |
| 2 | Create database schema (urls + clicks + rate_limits) | None |
| 3 | Build URL creation (generate code, validate, save) | Task 2 |
| 4 | Build redirect (lookup, check limits/expiry/password) | Task 2 |
| 5 | Add click tracking | Task 4 |
| 6 | Build analytics endpoint | Task 5 |
| 7 | Add click limit feature | Task 5 |
| 8 | Add expiration feature | Task 3 |
| 9 | Add password protection | Task 3 |
| 10 | Add bulk creation endpoint | Task 3 |
| 11 | Add rate limiting | Task 3 |
| 12 | Add URL blocking | Task 3 |
| 13 | Write tests (26 tests) | Tasks 3-12 |
| 14 | Write documentation | Task 13 |

## Step 3: Architecture

Simple 3-layer design:

```
HTTP Request
    ↓
Routes (routes.py)      → Handles HTTP, validates input via Pydantic
    ↓
Service (service.py)    → Business logic (no HTTP knowledge)
    ↓
Database (database.py)  → SQLite queries, data storage
```

## Step 4: What I Built

- **8 API endpoints** covering all features
- **26 automated tests** covering happy paths and error cases
- **Input validation** using Pydantic
- **Security features** (rate limiting, URL blocking, password hashing)
- **Auto-generated API docs** at `/docs` (Swagger UI)

## Step 5: What I Would Add for Production

- Authentication (API keys per user)
- Redis cache for hot URLs
- PostgreSQL instead of SQLite
- Background job to clean expired URLs
- Docker containerization
- Monitoring & alerting
- HTTPS termination
