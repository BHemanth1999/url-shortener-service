import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "urls.db")


def get_db():
    """Get a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, short_code TEXT UNIQUE NOT NULL, original_url TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP, max_clicks INTEGER, password TEXT, is_active INTEGER DEFAULT 1)")
    conn.execute("CREATE TABLE IF NOT EXISTS clicks (id INTEGER PRIMARY KEY AUTOINCREMENT, url_id INTEGER NOT NULL, clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ip_address TEXT, user_agent TEXT, referrer TEXT, FOREIGN KEY (url_id) REFERENCES urls(id))")
    conn.execute("CREATE TABLE IF NOT EXISTS rate_limits (ip_address TEXT NOT NULL, request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    return conn


def create_tables():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            max_clicks INTEGER,
            password TEXT,
            is_active INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER NOT NULL,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            referrer TEXT,
            FOREIGN KEY (url_id) REFERENCES urls(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rate_limits (
            ip_address TEXT NOT NULL,
            request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
