"""
Hands-On 8 [Advanced] - RESTful API Design Best Practices
TASK 2: Versioning, Pagination and Standardised Error Responses

Course Management API - FastAPI implementation (standalone, builds on the
same fixes from Task 1: plural nouns, correct HTTP methods/status codes,
Location header on POST). This file additionally adds:

  1. API VERSIONING
     Strategy used here: URL versioning -> every route lives under /api/v1/...
       + simple, visible right in the URL, trivial to test in a browser/curl/Postman
       - every breaking change forces a new prefix (v2, v3, ...) and, often,
         maintaining two versions of the router side by side for a while

     Alternative: header-based versioning, e.g.
       Accept: application/vnd.courseapi+json;version=1
       + keeps URLs clean and stable — the resource identity never changes
       - harder to test manually (can't just paste a URL into a browser),
         requires clients to set a custom header correctly on every request

  2. PAGINATION (offset/page based - the DRF-style envelope)
     GET /api/v1/courses/?page=1&page_size=2 ->
       {"count": <total>, "next": <url|null>, "previous": <url|null>, "results": [...]}

  3. FILTERING
     GET /api/v1/courses/?search=data  -> case-insensitive LIKE on name/code
     GET /api/v1/courses/?department_id=1 -> exact match filter

  4. STANDARDISED ERROR RESPONSES
     Every error (404, 400, 422, ...) is reshaped into:
       {"error": {"code": "NOT_FOUND", "message": "...", "field": null}}
     via global exception handlers below, instead of FastAPI's default
     {"detail": "..."} / {"detail": [...]} shapes.
"""

import math
from typing import Optional

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="Hands-On 8 / Task 2 - Versioning, pagination, filtering & standardised errors",
    version="1.0.0",
)

v1 = APIRouter(prefix="/api/v1")


# ============================================================ Error handling

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
    """Reshape every HTTPException into the standard {'error': {...}} envelope."""
    code = STATUS_CODE_TO_ERROR_CODE.get(exc.status_code, "ERROR")
    payload = schemas.ErrorResponse(
        error=schemas.ErrorDetail(code=code, message=str(exc.detail), field=None)
    )
    return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Reshape Pydantic/FastAPI's 422 validation errors into the standard envelope."""
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


# ============================================================ Pagination helper

def paginate(request: Request, query, page: int, page_size: int):
    """Offset pagination -> {'count', 'next', 'previous', 'results'} (DRF-style envelope)."""
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page_size must be between 1 and 100")

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    base_url = str(request.url).split("?")[0]
    total_pages = math.ceil(total / page_size) if page_size else 1

    next_url = f"{base_url}?page={page + 1}&page_size={page_size}" if page < total_pages else None
    previous_url = f"{base_url}?page={page - 1}&page_size={page_size}" if page > 1 else None

    return {"count": total, "next": next_url, "previous": previous_url, "results": items}


@v1.get("/", tags=["Root"])
def root():
    return {"message": "Course Management API v1 is running"}


# ============================================================ Departments

@v1.post(
    "/departments/",
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


@v1.get("/departments/", response_model=list[schemas.DepartmentResponse], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


# ============================================================ Courses (paginated + searchable)

@v1.get("/courses/", tags=["Courses"])
def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Paginated, filterable course list.
    ?search=data           -> case-insensitive LIKE on name OR code
    ?department_id=1       -> exact-match filter
    ?page=1&page_size=10   -> pagination
    """
    query = db.query(models.Course)

    if search:
        like = f"%{search}%"
        query = query.filter(or_(models.Course.name.ilike(like), models.Course.code.ilike(like)))

    if department_id is not None:
        query = query.filter(models.Course.department_id == department_id)

    result = paginate(request, query, page, page_size)
    result["results"] = [schemas.CourseResponse.model_validate(c) for c in result["results"]]
    return result


@v1.post(
    "/courses/",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
def create_course(course: schemas.CourseCreate, response: Response, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == course.department_id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="department_id does not exist")

    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code must be unique")
    db.refresh(db_course)

    response.headers["Location"] = f"/api/v1/courses/{db_course.id}/"
    return db_course


@v1.get("/courses/{course_id}/", response_model=schemas.CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} does not exist")
    return course


@v1.put("/courses/{course_id}/", response_model=schemas.CourseResponse, tags=["Courses"])
def replace_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} does not exist")

    for field, value in course.model_dump().items():
        setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course


@v1.patch("/courses/{course_id}/", response_model=schemas.CourseResponse, tags=["Courses"])
def update_course(course_id: int, course: schemas.CoursePatch, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} does not exist")

    for field, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course


@v1.delete("/courses/{course_id}/", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} does not exist")
    db.delete(db_course)
    db.commit()
    return None


# ============================================================ Students (paginated)

@v1.get("/students/", tags=["Students"])
def list_students(request: Request, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.Student)
    result = paginate(request, query, page, page_size)
    result["results"] = [schemas.StudentResponse.model_validate(s) for s in result["results"]]
    return result


@v1.post(
    "/students/",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: schemas.StudentCreate, response: Response, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be unique")
    db.refresh(db_student)

    response.headers["Location"] = f"/api/v1/students/{db_student.id}/"
    return db_student


@v1.get("/students/{student_id}/", response_model=schemas.StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {student_id} does not exist")
    return student


# ============================================================ Enrollments (paginated)

@v1.get("/enrollments/", tags=["Enrollments"])
def list_enrollments(request: Request, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.Enrollment)
    result = paginate(request, query, page, page_size)
    result["results"] = [schemas.EnrollmentResponse.model_validate(e) for e in result["results"]]
    return result


@v1.post(
    "/enrollments/",
    response_model=schemas.EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
def create_enrollment(enrollment: schemas.EnrollmentCreate, response: Response, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not student or not course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="student_id or course_id does not exist")

    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is already enrolled in this course")
    db.refresh(db_enrollment)

    response.headers["Location"] = f"/api/v1/enrollments/{db_enrollment.id}/"
    return db_enrollment


@v1.delete("/enrollments/{enrollment_id}/", status_code=status.HTTP_204_NO_CONTENT, tags=["Enrollments"])
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Enrollment with id {enrollment_id} does not exist")
    db.delete(db_enrollment)
    db.commit()
    return None


app.include_router(v1)
