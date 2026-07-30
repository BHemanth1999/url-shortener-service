import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import create_tables, DB_PATH
import os


@pytest.fixture(autouse=True)
def setup_db():
    """Create fresh tables before each test."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_tables()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


client = TestClient(app)


# ===== GREENFIELD: Core URL Shortener =====

def test_create_short_url():
    response = client.post("/api/urls", json={"url": "https://www.google.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == "https://www.google.com"


def test_create_with_custom_code():
    response = client.post("/api/urls", json={"url": "https://github.com", "custom_code": "github"})
    assert response.status_code == 201
    assert response.json()["short_code"] == "github"


def test_create_invalid_url():
    response = client.post("/api/urls", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_create_duplicate_code():
    client.post("/api/urls", json={"url": "https://a.com", "custom_code": "taken"})
    response = client.post("/api/urls", json={"url": "https://b.com", "custom_code": "taken"})
    assert response.status_code == 409


def test_redirect():
    client.post("/api/urls", json={"url": "https://www.example.com", "custom_code": "test123"})
    response = client.get("/test123", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.example.com"


def test_redirect_not_found():
    response = client.get("/doesnotexist", follow_redirects=False)
    assert response.status_code == 404


def test_analytics():
    client.post("/api/urls", json={"url": "https://example.com", "custom_code": "stats"})
    client.get("/stats", follow_redirects=False)
    client.get("/stats", follow_redirects=False)

    response = client.get("/api/urls/stats/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] == 2
    assert data["short_code"] == "stats"


def test_analytics_not_found():
    response = client.get("/api/urls/noexist/analytics")
    assert response.status_code == 404


def test_list_urls():
    client.post("/api/urls", json={"url": "https://a.com"})
    client.post("/api/urls", json={"url": "https://b.com"})

    response = client.get("/api/urls")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2


def test_delete_url():
    client.post("/api/urls", json={"url": "https://delete.com", "custom_code": "del-me"})
    response = client.delete("/api/urls/del-me")
    assert response.status_code == 204

    response = client.get("/del-me", follow_redirects=False)
    assert response.status_code == 404


def test_delete_not_found():
    response = client.delete("/api/urls/noexist")
    assert response.status_code == 404


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ===== BROWNFIELD: Click Limit Feature =====

def test_create_with_click_limit():
    response = client.post("/api/urls", json={
        "url": "https://limited.com",
        "custom_code": "limited",
        "max_clicks": 3
    })
    assert response.status_code == 201
    assert response.json()["max_clicks"] == 3


def test_click_limit_works():
    client.post("/api/urls", json={
        "url": "https://limited.com",
        "custom_code": "limit3",
        "max_clicks": 3
    })

    assert client.get("/limit3", follow_redirects=False).status_code == 302
    assert client.get("/limit3", follow_redirects=False).status_code == 302
    assert client.get("/limit3", follow_redirects=False).status_code == 302
    assert client.get("/limit3", follow_redirects=False).status_code == 404


def test_click_limit_shows_in_analytics():
    client.post("/api/urls", json={
        "url": "https://example.com",
        "custom_code": "track",
        "max_clicks": 5
    })
    client.get("/track", follow_redirects=False)

    response = client.get("/api/urls/track/analytics")
    data = response.json()
    assert data["max_clicks"] == 5
    assert data["clicks_remaining"] == 4


def test_no_click_limit_works_forever():
    client.post("/api/urls", json={"url": "https://forever.com", "custom_code": "forever"})
    for _ in range(10):
        assert client.get("/forever", follow_redirects=False).status_code == 302


# ===== BROWNFIELD: URL Expiration =====

def test_create_with_expiration():
    response = client.post("/api/urls", json={
        "url": "https://example.com",
        "custom_code": "expiry",
        "expires_in_hours": 24
    })
    assert response.status_code == 201
    assert response.json()["expires_at"] is not None


def test_non_expired_url_works():
    client.post("/api/urls", json={
        "url": "https://example.com",
        "custom_code": "fresh",
        "expires_in_hours": 24
    })
    response = client.get("/fresh", follow_redirects=False)
    assert response.status_code == 302


# ===== BROWNFIELD: Password Protection =====

def test_create_with_password():
    response = client.post("/api/urls", json={
        "url": "https://secret.com",
        "custom_code": "secret",
        "password": "mypass123"
    })
    assert response.status_code == 201
    assert response.json()["is_protected"] == True


def test_password_required_on_access():
    client.post("/api/urls", json={
        "url": "https://secret.com",
        "custom_code": "locked",
        "password": "pass123"
    })
    response = client.get("/locked", follow_redirects=False)
    assert response.status_code == 401


def test_wrong_password_rejected():
    client.post("/api/urls", json={
        "url": "https://secret.com",
        "custom_code": "locked2",
        "password": "correct"
    })
    response = client.get("/locked2?password=wrong", follow_redirects=False)
    assert response.status_code == 403


def test_correct_password_works():
    client.post("/api/urls", json={
        "url": "https://secret.com",
        "custom_code": "locked3",
        "password": "correct"
    })
    response = client.get("/locked3?password=correct", follow_redirects=False)
    assert response.status_code == 302


def test_unlock_endpoint():
    client.post("/api/urls", json={
        "url": "https://secret.com",
        "custom_code": "locked4",
        "password": "mypass"
    })
    response = client.post("/locked4/unlock", json={"password": "mypass"})
    assert response.status_code == 200
    assert response.json()["original_url"] == "https://secret.com"


# ===== BROWNFIELD: Bulk Creation =====

def test_bulk_create():
    response = client.post("/api/urls/bulk", json={
        "urls": ["https://google.com", "https://github.com", "https://python.org"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["created"] == 3
    assert len(data["results"]) == 3


def test_bulk_create_with_expiry():
    response = client.post("/api/urls/bulk", json={
        "urls": ["https://a.com", "https://b.com"],
        "expires_in_hours": 48
    })
    assert response.status_code == 201
    assert response.json()["created"] == 2


# ===== AMBIGUOUS (Security): Rate Limiting & URL Blocking =====

def test_blocked_domain_rejected():
    response = client.post("/api/urls", json={"url": "https://malware.com/bad-link"})
    assert response.status_code == 409
    assert "blocked" in response.json()["detail"].lower()


def test_safe_domain_allowed():
    response = client.post("/api/urls", json={"url": "https://google.com"})
    assert response.status_code == 201
