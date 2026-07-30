# Approach: How I Built This

## Requirement

> "Build a scalable URL shortener service with APIs, persistence, and analytics."

## Step 1: Breaking Down the Requirement

| Shorten a URL | Core functionality |
| Redirect with tracking | | Core + analytics |
| Click analytics | Explicitly requested |
| Click limit | Controlled distribution (brownfield) |
| URL expiration | Time-limited links (brownfield) |
| Password protection | Secure document sharing (brownfield) |
| Bulk creation | Marketing team efficiency |
| Rate limiting | Prevent abuse (security) |
| URL blocking | Prevent malicious links (security) |


## Step 2: Architecture

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

## Step 3: What I Built

- **8 API endpoints** covering all features
- **26 automated tests** covering happy paths and error cases
- **Input validation** using Pydantic
- **Security features** (rate limiting, URL blocking, password hashing)
- **Auto-generated API docs** at `/docs` (Swagger UI)

## Step 4: What I Would Add for Production

- Authentication (API keys per user)
- Redis cache for hot URLs
- PostgreSQL instead of SQLite
- Background job to clean expired URLs
- Docker containerization
- Monitoring & alerting
- HTTPS termination
