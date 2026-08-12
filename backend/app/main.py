from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import create_access_token, get_current_user, get_password_hash, verify_password
from app.database import Base, engine, get_db

app = FastAPI(title="JobSentinel API", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "JobSentinel API is running"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/db-status")
async def db_status(db: Session = Depends(get_db)) -> dict[str, str | int]:
    result = db.execute(text("SELECT 1"))
    value = result.scalar_one()
    return {"status": "connected", "result": value}


@app.get("/api/v1/test")
async def test_route() -> dict[str, str]:
    return {"message": "Backend structure is ready"}


@app.post("/api/v1/auth/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user = crud.create_user(db, payload.email, payload.full_name, get_password_hash(payload.password))
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/v1/auth/login", response_model=schemas.TokenResponse)
async def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash or ""):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/v1/me", response_model=schemas.UserRead)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@app.get("/api/v1/users", response_model=list[schemas.UserRead])
async def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/api/v1/companies")
async def read_companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)


@app.get("/api/v1/jobs")
async def read_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db)


@app.post("/api/v1/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return crud.create_user(db, payload.email, payload.full_name, get_password_hash(payload.password))


@app.post("/api/v1/companies", status_code=status.HTTP_201_CREATED)
async def create_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(
        db,
        name=payload.name,
        website=payload.website,
        industry=payload.industry,
        location=payload.location,
        notes=payload.notes,
    )


@app.post("/api/v1/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(payload: schemas.JobCreate, db: Session = Depends(get_db)):
    job_data = payload.model_dump()
    return crud.create_job(db, job_data)


@app.post("/api/v1/applications", status_code=status.HTTP_201_CREATED)
async def create_application(payload: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(
        db,
        user_id=payload.user_id,
        job_id=payload.job_id,
        application_status=payload.application_status,
        notes=payload.notes,
    )


@app.post("/api/v1/notifications", status_code=status.HTTP_201_CREATED)
async def create_notification(payload: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud.create_notification(
        db,
        user_id=payload.user_id,
        title=payload.title,
        message=payload.message,
        notification_type=payload.notification_type,
    )
