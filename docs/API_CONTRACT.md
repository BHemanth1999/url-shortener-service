# API Contract

Base URL: `http://localhost:8000`

Auto-generated interactive docs: `http://localhost:8000/docs` (Swagger UI)

---

## 1. Create Short URL

```
POST /api/urls
```

**Request:**
```json
{
  "url": "https://www.google.com",
  "custom_code": "goog",           // optional (3-20 chars)
  "max_clicks": 5,                 // optional (link dies after N clicks)
  "expires_in_hours": 48,          // optional (link dies after X hours)
  "password": "secret123"          // optional (password to access)
}
```

**Response (201 Created):**
```json
{
  "short_code": "goog",
  "short_url": "http://localhost:8000/goog",
  "original_url": "https://www.google.com",
  "created_at": "2026-07-29 10:00:00",
  "max_clicks": 5,
  "expires_at": "2026-07-31 10:00:00",
  "is_protected": false
}
```

**Errors:**
| Code | Meaning |
|------|---------|
| 409 | Short code already exists OR URL is blocked |
| 422 | Invalid URL or invalid input format |
| 429 | Rate limit exceeded (max 10/minute) |

---

## 2. Bulk Create URLs

```
POST /api/urls/bulk
```

**Request:**
```json
{
  "urls": ["https://google.com", "https://github.com", "https://python.org"],
  "expires_in_hours": 72    // optional (applies to all)
}
```

**Response (201 Created):**
```json
{
  "created": 3,
  "results": [
    {"short_code": "abc1234", "short_url": "http://localhost:8000/abc1234", "original_url": "https://google.com", ...},
    {"short_code": "xyz5678", "short_url": "http://localhost:8000/xyz5678", "original_url": "https://github.com", ...},
    {"short_code": "def9012", "short_url": "http://localhost:8000/def9012", "original_url": "https://python.org", ...}
  ]
}
```

**Errors:**
| Code | Meaning |
|------|---------|
| 422 | Invalid URL in list, or more than 50 URLs |
| 429 | Rate limit exceeded |

---

## 3. Redirect (Visit Short URL)

```
GET /{short_code}
```

**Success:** 301 Redirect to original URL

**With password:** `GET /{short_code}?password=secret123`

**Errors:**
| Code | Meaning |
|------|---------|
| 401 | Password required (link is protected) |
| 403 | Wrong password |
| 404 | Not found, expired, or click limit reached |

---

## 4. Unlock Password-Protected URL

```
POST /{short_code}/unlock
```

**Request:**
```json
{
  "password": "secret123"
}
```

**Response (200 OK):**
```json
{
  "original_url": "https://secret-document.com"
}
```

**Errors:**
| Code | Meaning |
|------|---------|
| 403 | Wrong password |
| 404 | Not found, expired, or click limit reached |

---

## 5. Get Analytics

```
GET /api/urls/{short_code}/analytics
```

**Response (200 OK):**
```json
{
  "short_code": "goog",
  "original_url": "https://www.google.com",
  "total_clicks": 42,
  "max_clicks": 100,
  "clicks_remaining": 58,
  "expires_at": "2026-07-31 10:00:00",
  "is_expired": false,
  "created_at": "2026-07-29 10:00:00",
  "clicks_by_date": [
    {"date": "2026-07-29", "count": 30},
    {"date": "2026-07-28", "count": 12}
  ],
  "recent_clicks": [
    {"clicked_at": "2026-07-29 14:30:00", "ip": "192.168.1.1", "user_agent": "Chrome", "referrer": "google.com"}
  ]
}
```

**Errors:**
| Code | Meaning |
|------|---------|
| 404 | Short code not found |

---

## 6. List All URLs

```
GET /api/urls?page=1&limit=10
```

**Response (200 OK):**
```json
{
  "urls": [
    {"short_code": "goog", "short_url": "...", "original_url": "...", "created_at": "...", "max_clicks": null, "expires_at": null, "is_protected": false}
  ],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

---

## 7. Delete URL

```
DELETE /api/urls/{short_code}
```

**Response:** 204 No Content (success, no body)

**Errors:**
| Code | Meaning |
|------|---------|
| 404 | Short code not found |

---

## 8. Health Check

```
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## HTTP Status Codes Used

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET request |
| 201 | Created | New URL created |
| 204 | No Content | Successful delete |
| 301 | Redirect | Short URL → original URL |
| 401 | Unauthorized | Password required |
| 403 | Forbidden | Wrong password |
| 404 | Not Found | URL doesn't exist, expired, or limit reached |
| 409 | Conflict | Duplicate code or blocked domain |
| 422 | Validation Error | Bad input (invalid URL, bad format) |
| 429 | Too Many Requests | Rate limit exceeded |

---

## Database Schema

### urls table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment primary key |
| short_code | TEXT (unique) | The short code (e.g. "goog") |
| original_url | TEXT | The full original URL |
| created_at | TIMESTAMP | When it was created |
| expires_at | TIMESTAMP | When it expires (null = never) |
| max_clicks | INTEGER | Max allowed clicks (null = unlimited) |
| password | TEXT | Hashed password (null = not protected) |
| is_active | INTEGER | 1 = active, 0 = deleted |

### clicks table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment primary key |
| url_id | INTEGER (FK) | Links to urls.id |
| clicked_at | TIMESTAMP | When the click happened |
| ip_address | TEXT | Visitor's IP |
| user_agent | TEXT | Visitor's browser |
| referrer | TEXT | Where they came from |

### rate_limits table
| Column | Type | Description |
|--------|------|-------------|
| ip_address | TEXT | Requester's IP |
| request_time | TIMESTAMP | When the request was made |
