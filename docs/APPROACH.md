# Approach: How I Built This

## Requirement

> "Build a scalable URL shortener service with APIs, persistence, and analytics."

## Step 1: Breaking Down the Requirement
- **Shorten a URL** 
- **Bulk creation** 
- **Analytics** 
- **Delete URL** 
- **Password Protection** 
- **Rate Limiting**


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
