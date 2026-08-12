from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Application, Company, Job, Notification, User


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(User).offset(skip).limit(limit)).scalars().all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Company).offset(skip).limit(limit)).scalars().all()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Job).offset(skip).limit(limit)).scalars().all()


def create_user(db: Session, email: str, full_name: str, password_hash: str | None = None):
    user = User(email=email, full_name=full_name, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_company(db: Session, name: str, website: str | None = None, industry: str | None = None, location: str | None = None, notes: str | None = None):
    company = Company(name=name, website=website, industry=industry, location=location, notes=notes)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def create_job(db: Session, job_data: dict):
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def create_application(db: Session, user_id: int, job_id: int, application_status: str = "applied", notes: str | None = None):
    application = Application(user_id=user_id, job_id=job_id, application_status=application_status, notes=notes)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def create_notification(db: Session, user_id: int, title: str, message: str, notification_type: str | None = None):
    notification = Notification(user_id=user_id, title=title, message=message, notification_type=notification_type)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
