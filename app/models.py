from pydantic import BaseModel, field_validator
from typing import Optional
from urllib.parse import urlparse


class CreateUrlRequest(BaseModel):
    url: str
    custom_code: Optional[str] = None
    max_clicks: Optional[int] = None
    expires_in_hours: Optional[int] = None
    expires_in_seconds: Optional[int] = None
    password: Optional[str] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL must start with http:// or https://")
        if not parsed.netloc:
            raise ValueError("Invalid URL format")
        return v

    @field_validator("custom_code")
    @classmethod
    def validate_custom_code(cls, v):
        if v is None:
            return v
        if len(v) < 3 or len(v) > 20:
            raise ValueError("Custom code must be 3-20 characters")
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Custom code: only letters, numbers, - and _ allowed")
        return v

    @field_validator("max_clicks")
    @classmethod
    def validate_max_clicks(cls, v):
        if v is None:
            return v
        if v < 1:
            raise ValueError("max_clicks must be at least 1")
        return v

    @field_validator("expires_in_hours")
    @classmethod
    def validate_expires(cls, v):
        if v is None:
            return v
        if v < 1:
            raise ValueError("expires_in_hours must be at least 1")
        return v

    @field_validator("expires_in_seconds")
    @classmethod
    def validate_expires_seconds(cls, v):
        if v is None:
            return v
        if v < 5:
            raise ValueError("expires_in_seconds must be at least 5")
        return v


class BulkCreateRequest(BaseModel):
    urls: list[str]
    expires_in_hours: Optional[int] = None

    @field_validator("urls")
    @classmethod
    def validate_urls(cls, v):
        if len(v) == 0:
            raise ValueError("At least one URL required")
        if len(v) > 50:
            raise ValueError("Maximum 50 URLs per batch")
        for url in v:
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError(f"Invalid URL: {url}")
        return v


class PasswordRequest(BaseModel):
    password: str


class UrlResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: str
    max_clicks: Optional[int] = None
    expires_at: Optional[str] = None
    is_protected: bool = False


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    max_clicks: Optional[int] = None
    clicks_remaining: Optional[int] = None
    expires_at: Optional[str] = None
    is_expired: bool = False
    created_at: str
    clicks_by_date: list[dict]
    recent_clicks: list[dict]
