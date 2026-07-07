"""
Hands-On 9 [Advanced] - Authentication & Security - JWT, OAuth2 & OWASP
TASK 2: JWT Login, Protected Routes and CORS

Implements:
  - POST /api/v1/auth/register/    (carried over from Task 1)
  - POST /api/v1/auth/login/       accepts email+password, verifies via
                                    verify_password(), issues a JWT with a
                                    30-minute expiry                          [step 91]
  - get_current_user()             dependency that decodes/validates the JWT
                                    and returns the current User, or 401      [step 92]
  - POST /api/v1/courses/ and
    DELETE /api/v1/courses/{id}/   require Depends(get_current_user)         [step 93]
    (GET stays public / unauthenticated)
  - CORSMiddleware                 allows http://localhost:3000              [step 94]
  - OAuth2 Authorization Code flow vs. this simple JWT login                 [step 95]
    -- see the docstring on the login route below.
"""

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, get_db
from security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API - Auth",
    description="Hands-On 9 / Task 2 - JWT login, protected routes & CORS",
    version="1.0.0",
)

# ============================================================ CORS  [step 94]
# Allows the frontend dev server (http://localhost:3000) to call this API
# from the browser. Reminder: CORS is enforced by the BROWSER, not the
# server - it does not protect server-to-server calls (curl, Postman, other
# backends can call this API regardless of CORS settings). It only stops a
# browser page served from a different origin from reading the response.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# tokenUrl points Swagger's "Authorize" button at the login route below.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


# ============================================================ Standardised errors

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
    payload = schemas.ErrorResponse(error=schemas.ErrorDetail(code=code, message=str(exc.detail), field=None))
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload), headers=exc.headers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first = errors[0] if errors else {}
    field = ".".join(str(p) for p in first.get("loc", [])[1:]) or None
    payload = schemas.ErrorResponse(
        error=schemas.ErrorDetail(code="UNPROCESSABLE_ENTITY", message=first.get("msg", "Validation error"), field=field)
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(payload))


@app.get("/", tags=["Root"])
def root():
    return {"message": "Auth service is running"}


# ============================================================ get_current_user  [step 92]

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Decode and validate the bearer JWT. Raises 401 if the token is missing,
    malformed, tampered with, expired, or refers to a user that no longer
    exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# ============================================================ Auth routes

@app.post(
    "/api/v1/auth/register/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
)
def register(user: schemas.UserRegister, response: Response, db: Session = Depends(get_db)):
    """Carried over from Task 1: hash the password, 409 on duplicate email."""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, f"A user with email '{user.email}' is already registered")

    db_user = models.User(email=user.email, hashed_password=get_password_hash(user.password), is_active=True)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, f"A user with email '{user.email}' is already registered")
    db.refresh(db_user)

    response.headers["Location"] = f"/api/v1/users/{db_user.id}/"
    return db_user


@app.post("/api/v1/auth/login/", response_model=schemas.Token, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Simple JWT ("password") login: client sends email (as `username`) +
    password directly, server verifies and returns a signed JWT.

    OAuth2PasswordRequestForm is used (rather than a plain JSON body) purely
    so Swagger's built-in "Authorize" button works out of the box for
    testing - it still just reads two form fields: username & password.

    step 95 - how this differs from the OAuth2 Authorization Code flow:
      This "password" grant trusts the client to collect the user's raw
      credentials and send them straight to this API in one request - fine
      for a first-party app talking to its own backend, but it means any
      client integrating this way must be trusted with the user's actual
      password.

      The Authorization Code flow (used for "Sign in with Google/GitHub"
      style buttons and third-party clients) never lets the client see the
      password at all:
        1. Client redirects the user's browser to the auth server's
           /authorize endpoint.
        2. The user logs in and consents on the auth server's own page
           (not the client's).
        3. The auth server redirects back to the client with a short-lived
           one-time `code`.
        4. The client exchanges that `code` (plus its own client_secret)
           for an access token via a server-to-server call to /token.
      This flow keeps credentials confined to the auth server and lets a
      third party integrate without ever handling the user's password -
      at the cost of more moving parts (redirects, a `code` exchange step,
      registered redirect URIs, etc.) than the direct login used here.
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/api/v1/users/me/", response_model=schemas.UserResponse, tags=["Auth"])
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """Simplest possible protected route - proves the token round-trips correctly."""
    return current_user


# ============================================================ Departments (support resource)

@app.post(
    "/api/v1/departments/",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Departments"],
)
def create_department(department: schemas.DepartmentCreate, response: Response, db: Session = Depends(get_db)):
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    response.headers["Location"] = f"/api/v1/departments/{db_department.id}/"
    return db_department


# ============================================================ Courses  [step 93: POST/DELETE protected]

@app.get("/api/v1/courses/", response_model=list[schemas.CourseResponse], tags=["Courses"])
def list_courses(db: Session = Depends(get_db)):
    """Public - no auth required."""
    return db.query(models.Course).all()


@app.post(
    "/api/v1/courses/",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
def create_course(
    course: schemas.CourseCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Protected - requires a valid bearer token. Unauthenticated requests get 401."""
    department = db.query(models.Department).filter(models.Department.id == course.department_id).first()
    if not department:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "department_id does not exist")

    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Course code must be unique")
    db.refresh(db_course)

    response.headers["Location"] = f"/api/v1/courses/{db_course.id}/"
    return db_course


@app.delete("/api/v1/courses/{course_id}/", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Protected - requires a valid bearer token. Unauthenticated requests get 401."""
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Course with id {course_id} does not exist")
    db.delete(db_course)
    db.commit()
    return None
