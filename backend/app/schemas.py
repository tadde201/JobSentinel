from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    user_id: int
    email: str
    full_name: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyCreate(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class JobCreate(BaseModel):
    company_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    remote_type: Optional[str] = None
    employment_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    url: str
    source: Optional[str] = None
    external_job_id: Optional[str] = None
    posted_date: Optional[datetime] = None
    status: str = "active"


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    application_status: str = "applied"
    applied_at: Optional[datetime] = None
    notes: Optional[str] = None


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    notification_type: Optional[str] = None
