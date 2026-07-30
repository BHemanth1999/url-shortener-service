# Key Decisions & Trade-offs

## Decision 1: Python + FastAPI

| Considered | Chose | Why |
|-----------|-------|-----|
| Flask | FastAPI | Auto-generates Swagger docs, built-in validation |
| Express (Node.js) | FastAPI | Python simpler for this scope |
| Django | FastAPI | Django too heavy for a microservice |

## Decision 2: SQLite over PostgreSQL

| Factor | SQLite | PostgreSQL |
|--------|--------|-----------|
| Setup | Zero (file) | Needs server |
| Portability | Just copy folder | Needs connection |
| Performance | Good for thousands | Needed for millions |

**Why SQLite:** Zero setup, anyone can run it instantly. Production path: swap to PostgreSQL (same SQL).

## Decision 3: Random Short Codes

| Approach | Pros | Cons |
|----------|------|------|
| Random 7 chars (chose) | Simple, unpredictable | Tiny collision risk |
| Sequential base62 | No collisions | Predictable URLs |
| Hash of URL | Same URL = same code | Longer, collision risk |

**Why random:** 62^7 = 3.5 trillion combinations. Unpredictable = more secure.

## Decision 4: Password Hashing (SHA-256)

Passwords are hashed before storage — never stored in plain text.

**Why:** Even if database is leaked, passwords can't be read. Standard security practice.

**Production upgrade:** Use bcrypt instead of SHA-256 (slower = harder to brute force).

## Decision 5: Soft Delete

URLs marked `is_active = 0` instead of deleted from database.

**Why:** Preserves click history for auditing. Can restore if needed. Important in financial contexts.

## Decision 6: Rate Limiting in Database

Rate limits tracked in SQLite (not in-memory).

**Trade-off:**
- Pro: Survives server restart, simple implementation
- Con: Slightly slower than Redis
- **Production:** Use Redis for rate limiting

## Decision 7: Click Limit Check on Access

Click count checked every time someone accesses the URL.

**Trade-off:**
- Pro: Always accurate, no stale state
- Con: Extra DB query per redirect
- Acceptable because: SQLite reads are fast (<1ms)

## Assumptions

1. Single server deployment
2. Moderate traffic (not millions of requests/second)
3. URLs are public by default (password optional)
4. Short codes are 7 characters
5. Rate limit: 10 requests per minute per IP
6. Blocked domains list is static (hardcoded)

## Known Limitations

| Limitation | Impact | Why acceptable |
|-----------|--------|---------------|
| No auth | Anyone can create URLs | Demo scope |
| SQLite single writer | Slow under heavy writes | Demo scale |
| Static blocklist | Can't catch new threats | Would use external API in production |
| SHA-256 for passwords | Fast hash (brute-forceable) | Would use bcrypt in production |
| No background cleanup | Expired URLs stay in DB | Would add cron job in production |
| IP-based rate limit | VPN bypass possible | Would add API keys in production |
