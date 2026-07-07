"""
Hands-On 9 [Advanced] - Authentication & Security - JWT, OAuth2 & OWASP
TASK 1: Password Hashing and User Registration

Implements:
  - User model (id, email [unique], hashed_password, is_active)              [step 86]
  - security.py: get_password_hash() / verify_password() via passlib+bcrypt  [step 87]
  - POST /api/v1/auth/register/                                              [step 88]
      - validates email format (Pydantic EmailStr does this automatically)
      - checks the email isn't already registered -> 409 Conflict if so
      - hashes the password with bcrypt before saving
  - Plain-text passwords are never stored or logged                          [step 89]
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, get_db
from security import get_password_hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API - Auth",
    description="Hands-On 9 / Task 1 - Password hashing & user registration",
    version="1.0.0",
)


# ============================================================ Standardised errors
# (same envelope pattern used in Hands-On 8 / Task 2)

STATUS_CODE_TO_ERROR_CODE = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "UNPROCESSABLE_ENTITY",
    500: "INTERNAL_SERVER_ERROR",
}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code = STATUS_CODE_TO_ERROR_CODE.get(exc.status_code, "ERROR")
    payload = schemas.ErrorResponse(
        error=schemas.ErrorDetail(code=code, message=str(exc.detail), field=None)
    )
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first = errors[0] if errors else {}
    field = ".".join(str(p) for p in first.get("loc", [])[1:]) or None
    payload = schemas.ErrorResponse(
        error=schemas.ErrorDetail(
            code="UNPROCESSABLE_ENTITY",
            message=first.get("msg", "Validation error"),
            field=field,
        )
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(payload))


@app.get("/", tags=["Root"])
def root():
    return {"message": "Auth service is running"}


# ============================================================ Registration

@app.post(
    "/api/v1/auth/register/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
)
def register(user: schemas.UserRegister, response: Response, db: Session = Depends(get_db)):
    """
    Register a new user.

    - EmailStr on the request schema rejects malformed emails with a 422
      before this function body even runs.
    - An existing email returns 409 Conflict (not 400) - the request is
      well-formed, it simply conflicts with existing state.
    - The password is hashed with bcrypt via get_password_hash() and only
      the resulting hash is written to the database. The plain-text
      `user.password` value is used exactly once, right here, and is never
      logged or persisted.
    """
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email '{user.email}' is already registered",
        )

    hashed = get_password_hash(user.password)

    db_user = models.User(email=user.email, hashed_password=hashed, is_active=True)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        # Belt-and-braces: guards against a race between the check above and
        # the insert (two concurrent registrations with the same email).
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email '{user.email}' is already registered",
        )
    db.refresh(db_user)

    response.headers["Location"] = f"/api/v1/users/{db_user.id}/"
    return db_user


@app.get(
    "/api/v1/users/{user_id}/",
    response_model=schemas.UserResponse,
    tags=["Auth"],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Read-only lookup used to confirm registration worked (and that the
    hashed_password field is never exposed via the API)."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not exist")
    return db_user
