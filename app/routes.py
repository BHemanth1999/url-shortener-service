from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from app.models import CreateUrlRequest, BulkCreateRequest, PasswordRequest, UrlResponse, AnalyticsResponse
from app import service

router = APIRouter()


@router.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/api/urls", response_model=UrlResponse, status_code=201)
def create_url(body: CreateUrlRequest, request: Request):
    """Create a new short URL. Options: max_clicks, expires_in_hours, password."""
    ip = request.client.host if request.client else "unknown"
    if not service.check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Max 10 requests per minute.")

    try:
        result = service.create_short_url(
            body.url, body.custom_code, body.max_clicks,
            body.expires_in_hours, body.expires_in_seconds, body.password
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/api/urls/bulk", status_code=201)
def bulk_create_urls(body: BulkCreateRequest, request: Request):
    """Create multiple short URLs at once (max 50)."""
    ip = request.client.host if request.client else "unknown"
    if not service.check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")

    results = service.bulk_create_urls(body.urls, body.expires_in_hours)
    return {"created": len([r for r in results if "error" not in r]), "results": results}


@router.get("/api/urls")
def list_urls(page: int = 1, limit: int = 10):
    """List all short URLs with pagination."""
    return service.list_urls(page, min(limit, 100))


@router.get("/api/urls/{short_code}/analytics", response_model=AnalyticsResponse)
def get_analytics(short_code: str):
    """Get click analytics for a short URL."""
    result = service.get_analytics(short_code)
    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return result


@router.delete("/api/urls/{short_code}", status_code=204)
def delete_url(short_code: str):
    """Delete a short URL (soft delete)."""
    if not service.delete_url(short_code):
        raise HTTPException(status_code=404, detail="Short URL not found")


@router.post("/{short_code}/unlock")
def unlock_protected_url(short_code: str, body: PasswordRequest):
    """Access a password-protected URL by providing the password."""
    original_url = service.get_original_url(short_code, password=body.password)

    if original_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found, expired, or click limit reached")
    if original_url == "WRONG_PASSWORD":
        raise HTTPException(status_code=403, detail="Wrong password")

    service.record_click(short_code)
    return {"original_url": original_url}


@router.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, password: str = Query(default=None)):
    """Redirect short URL to original URL. Add ?password=xxx for protected links."""
    original_url = service.get_original_url(short_code, password=password)

    if original_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found, expired, or click limit reached")
    if original_url == "PASSWORD_REQUIRED":
        raise HTTPException(status_code=401, detail="This URL is password-protected. Use POST /{code}/unlock with password, or add ?password=xxx")
    if original_url == "WRONG_PASSWORD":
        raise HTTPException(status_code=403, detail="Wrong password")

    service.record_click(
        short_code,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        referrer=request.headers.get("referrer"),
    )
    return RedirectResponse(url=original_url, status_code=302)
