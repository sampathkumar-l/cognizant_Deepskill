from typing import Optional

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Response,
    BackgroundTasks
)

from models import Course, Student
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    engine,
    Base,
    get_db
)

from models import Course

from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

from models import Student
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse
)

from models import (
    Course,
    Student,
    Enrollment
)

app = FastAPI(

    title="Course Management API",

    description="REST API for managing departments, courses, students and enrollments.",

    version="1.0.0",

    contact={
        "name": "Sampath Kumar",
        "email": "admin@college.edu"
    }

)


def send_confirmation_email(student_email: str):

    print(f"Sending confirmation email to {student_email}")

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)




@app.get("/")
async def root():

    return {
        "message": "API Running"
    }




@app.get(
    "/api/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)

async def get_courses(

    skip: int = 0,

    limit: int = 10,

    department_id: Optional[int] = None,

    db: AsyncSession = Depends(get_db)

):

    query = select(Course)

    if department_id is not None:

        query = query.where(
            Course.department_id == department_id
        )

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()




@app.get(

    "/api/courses/{course_id}",

    response_model=CourseResponse,

    tags=["Courses"]

)

async def get_course(

    course_id: int,

    db: AsyncSession = Depends(get_db)

):

    result = await db.execute(

        select(Course).where(

            Course.id == course_id

        )

    )

    course = result.scalar_one_or_none()

    if course is None:

        raise HTTPException(

            status_code=404,

            detail="Course not found"

        )

    return course




@app.post(

    "/api/courses/",

    response_model=CourseResponse,

    status_code=status.HTTP_201_CREATED,

    tags=["Courses"],

    summary="Create Course",

    response_description="Course created successfully"

)

async def create_course(

    course: CourseCreate,

    db: AsyncSession = Depends(get_db)

):

    new_course = Course(

        name=course.name,

        code=course.code,

        credits=course.credits,

        department_id=course.department_id

    )

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    headers = {

        "Location": f"/api/courses/{new_course.id}"

    }

    return JSONResponse(

        status_code=201,

        content={

            "id": new_course.id,

            "name": new_course.name,

            "code": new_course.code,

            "credits": new_course.credits,

            "department_id": new_course.department_id

        },

        headers=headers

    )




@app.put(

    "/api/courses/{course_id}",

    response_model=CourseResponse,

    tags=["Courses"]

)

async def update_course(

    course_id: int,

    course: CourseCreate,

    db: AsyncSession = Depends(get_db)

):

    result = await db.execute(

        select(Course).where(

            Course.id == course_id

        )

    )

    existing = result.scalar_one_or_none()

    if existing is None:

        raise HTTPException(

            status_code=404,

            detail="Course not found"

        )

    existing.name = course.name
    existing.code = course.code
    existing.credits = course.credits
    existing.department_id = course.department_id

    await db.commit()

    await db.refresh(existing)

    return existing




@app.patch(

    "/api/courses/{course_id}",

    response_model=CourseResponse,

    tags=["Courses"]

)

async def patch_course(

    course_id: int,

    course: CourseUpdate,

    db: AsyncSession = Depends(get_db)

):

    result = await db.execute(

        select(Course).where(

            Course.id == course_id

        )

    )

    existing = result.scalar_one_or_none()

    if existing is None:

        raise HTTPException(

            status_code=404,

            detail="Course not found"

        )

    updates = course.model_dump(

        exclude_unset=True

    )

    for key, value in updates.items():

        setattr(existing, key, value)

    await db.commit()

    await db.refresh(existing)

    return existing




@app.delete(

    "/api/courses/{course_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    tags=["Courses"]

)

async def delete_course(

    course_id: int,

    db: AsyncSession = Depends(get_db)

):

    result = await db.execute(

        select(Course).where(

            Course.id == course_id

        )

    )

    course = result.scalar_one_or_none()

    if course is None:

        raise HTTPException(

            status_code=404,

            detail="Course not found"

        )

    await db.delete(course)

    await db.commit()

    return Response(status_code=204)

@app.get(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.get(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.get(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@app.post(
    "/api/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        enrollment_year=student.enrollment_year,
        department_id=student.department_id
    )

    db.add(new_student)

    await db.commit()

    await db.refresh(new_student)

    return new_student

@app.put(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def update_student(
    student_id: int,
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    existing = result.scalar_one_or_none()

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing.first_name = student.first_name
    existing.last_name = student.last_name
    existing.email = student.email
    existing.enrollment_year = student.enrollment_year
    existing.department_id = student.department_id

    await db.commit()

    await db.refresh(existing)

    return existing

@app.patch(
    "/api/students/{student_id}",
    response_model=StudentResponse,
    tags=["Students"]
)
async def patch_student(
    student_id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    existing = result.scalar_one_or_none()

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    updates = student.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(existing, key, value)

    await db.commit()

    await db.refresh(existing)

    return existing

@app.delete(
    "/api/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"]
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    await db.delete(student)

    await db.commit()

    return Response(status_code=204)

@app.get(
    "/api/enrollments/",
    response_model=list[EnrollmentResponse],
    tags=["Enrollments"]
)
async def get_enrollments(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).offset(skip).limit(limit)
    )

    return result.scalars().all()

@app.get(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"]
)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    return enrollment

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
    summary="Enroll a student",
    response_description="Enrollment created successfully"
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db)
):

    new_enrollment = Enrollment(

        student_id=enrollment.student_id,

        course_id=enrollment.course_id,

        enrollment_date=enrollment.enrollment_date,

        grade=enrollment.grade

    )

    db.add(new_enrollment)

    await db.commit()

    await db.refresh(new_enrollment)

    return new_enrollment

@app.put(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"]
)
async def update_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    existing = result.scalar_one_or_none()

    if existing is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    existing.student_id = enrollment.student_id
    existing.course_id = enrollment.course_id
    existing.enrollment_date = enrollment.enrollment_date
    existing.grade = enrollment.grade

    await db.commit()

    await db.refresh(existing)

    return existing

@app.patch(
    "/api/enrollments/{enrollment_id}",
    response_model=EnrollmentResponse,
    tags=["Enrollments"]
)
async def patch_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    existing = result.scalar_one_or_none()

    if existing is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    updates = enrollment.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():

        setattr(existing, key, value)

    await db.commit()

    await db.refresh(existing)

    return existing

@app.delete(
    "/api/enrollments/{enrollment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Enrollments"]
)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.id == enrollment_id
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:

        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    await db.delete(enrollment)

    await db.commit()

    return Response(status_code=204)