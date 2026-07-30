import string
import random
import hashlib
from datetime import datetime, timedelta
from app.database import get_db

BASE_URL = "http://localhost:8000"
CHARS = string.ascii_letters + string.digits

BLOCKED_DOMAINS = ["malware.com", "phishing.net", "spam.org", "evil.com"]


def generate_short_code(length=7):
    """Generate a random short code."""
    return ''.join(random.choices(CHARS, k=length))


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_safe_url(url: str) -> bool:
    """Check if URL is not in blocked domains list."""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lower()
    return domain not in BLOCKED_DOMAINS


def check_rate_limit(ip: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
    """Check if IP has exceeded rate limit. Returns True if allowed."""
    conn = get_db()
    conn.execute(
        "DELETE FROM rate_limits WHERE request_time < datetime('now', ?)",
        (f"-{window_seconds} seconds",),
    )
    count = conn.execute(
        "SELECT COUNT(*) as count FROM rate_limits WHERE ip_address = ?",
        (ip,),
    ).fetchone()["count"]

    if count >= max_requests:
        conn.close()
        return False

    conn.execute("INSERT INTO rate_limits (ip_address) VALUES (?)", (ip,))
    conn.commit()
    conn.close()
    return True


def create_short_url(original_url: str, custom_code: str = None,
                     max_clicks: int = None, expires_in_hours: int = None,
                     expires_in_seconds: int = None, password: str = None) -> dict:
    """Create a new short URL."""
    if not is_safe_url(original_url):
        raise ValueError("URL is blocked - domain is not allowed")

    short_code = custom_code or generate_short_code()

    expires_at = None
    if expires_in_seconds:
        expires_at = (datetime.now() + timedelta(seconds=expires_in_seconds)).strftime("%Y-%m-%d %H:%M:%S")
    elif expires_in_hours:
        expires_at = (datetime.now() + timedelta(hours=expires_in_hours)).strftime("%Y-%m-%d %H:%M:%S")

    hashed_pw = hash_password(password) if password else None

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO urls (short_code, original_url, max_clicks, expires_at, password) VALUES (?, ?, ?, ?, ?)",
            (short_code, original_url, max_clicks, expires_at, hashed_pw),
        )
        conn.commit()
    except Exception as e:
        conn.close()
        if "UNIQUE" in str(e):
            raise ValueError("Short code already exists")
        raise e

    row = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    conn.close()

    return {
        "short_code": row["short_code"],
        "short_url": f"{BASE_URL}/{row['short_code']}",
        "original_url": row["original_url"],
        "created_at": row["created_at"],
        "max_clicks": row["max_clicks"],
        "expires_at": row["expires_at"],
        "is_protected": row["password"] is not None,
    }


def bulk_create_urls(urls: list[str], expires_in_hours: int = None) -> list[dict]:
    """Create multiple short URLs at once."""
    results = []
    for url in urls:
        try:
            result = create_short_url(url, expires_in_hours=expires_in_hours)
            results.append(result)
        except ValueError as e:
            results.append({"url": url, "error": str(e)})
    return results


def get_original_url(short_code: str, password: str = None) -> str:
    """Look up original URL. Returns None if not found, expired, or click limit reached."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM urls WHERE short_code = ? AND is_active = 1",
        (short_code,),
    ).fetchone()

    if not row:
        conn.close()
        return None

    # Check expiration
    if row["expires_at"]:
        if datetime.now() > datetime.strptime(row["expires_at"], "%Y-%m-%d %H:%M:%S"):
            conn.close()
            return None

    # Check click limit
    if row["max_clicks"] is not None:
        click_count = conn.execute(
            "SELECT COUNT(*) as count FROM clicks WHERE url_id = ?",
            (row["id"],),
        ).fetchone()["count"]
        if click_count >= row["max_clicks"]:
            conn.close()
            return None

    # Check password
    if row["password"] is not None:
        if password is None:
            conn.close()
            return "PASSWORD_REQUIRED"
        if hash_password(password) != row["password"]:
            conn.close()
            return "WRONG_PASSWORD"

    conn.close()
    return row["original_url"]


def record_click(short_code: str, ip: str = None, user_agent: str = None, referrer: str = None):
    """Record a click event for analytics."""
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()

    if row:
        conn.execute(
            "INSERT INTO clicks (url_id, ip_address, user_agent, referrer) VALUES (?, ?, ?, ?)",
            (row["id"], ip, user_agent, referrer),
        )
        conn.commit()
    conn.close()


def get_analytics(short_code: str) -> dict:
    """Get click analytics for a short URL."""
    conn = get_db()

    row = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()

    if not row:
        conn.close()
        return None

    total = conn.execute(
        "SELECT COUNT(*) as count FROM clicks WHERE url_id = ?", (row["id"],)
    ).fetchone()["count"]

    clicks_by_date = conn.execute(
        """SELECT date(clicked_at) as date, COUNT(*) as count
           FROM clicks WHERE url_id = ?
           GROUP BY date(clicked_at)
           ORDER BY date DESC LIMIT 30""",
        (row["id"],),
    ).fetchall()

    recent = conn.execute(
        """SELECT clicked_at, ip_address, user_agent, referrer
           FROM clicks WHERE url_id = ?
           ORDER BY clicked_at DESC LIMIT 10""",
        (row["id"],),
    ).fetchall()

    conn.close()

    max_clicks = row["max_clicks"]
    clicks_remaining = (max_clicks - total) if max_clicks else None

    is_expired = False
    if row["expires_at"]:
        is_expired = datetime.now() > datetime.strptime(row["expires_at"], "%Y-%m-%d %H:%M:%S")

    return {
        "short_code": short_code,
        "original_url": row["original_url"],
        "total_clicks": total,
        "max_clicks": max_clicks,
        "clicks_remaining": clicks_remaining,
        "expires_at": row["expires_at"],
        "is_expired": is_expired,
        "created_at": row["created_at"],
        "clicks_by_date": [{"date": r["date"], "count": r["count"]} for r in clicks_by_date],
        "recent_clicks": [
            {
                "clicked_at": r["clicked_at"],
                "ip": r["ip_address"],
                "user_agent": r["user_agent"],
                "referrer": r["referrer"],
            }
            for r in recent
        ],
    }


def delete_url(short_code: str) -> bool:
    """Soft-delete a URL."""
    conn = get_db()
    result = conn.execute(
        "UPDATE urls SET is_active = 0 WHERE short_code = ? AND is_active = 1",
        (short_code,),
    )
    conn.commit()
    deleted = result.rowcount > 0
    conn.close()
    return deleted


def list_urls(page: int = 1, limit: int = 10) -> dict:
    """List all active URLs with pagination."""
    offset = (page - 1) * limit
    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) as count FROM urls WHERE is_active = 1"
    ).fetchone()["count"]

    rows = conn.execute(
        "SELECT * FROM urls WHERE is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    conn.close()

    return {
        "urls": [
            {
                "short_code": r["short_code"],
                "short_url": f"{BASE_URL}/{r['short_code']}",
                "original_url": r["original_url"],
                "created_at": r["created_at"],
                "max_clicks": r["max_clicks"],
                "expires_at": r["expires_at"],
                "is_protected": r["password"] is not None,
            }
            for r in rows
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }
