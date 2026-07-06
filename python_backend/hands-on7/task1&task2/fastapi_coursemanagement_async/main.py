from typing import Optional
from fastapi import FastAPI,Depends,HTTPException,status,Response,BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine,Base,get_db
from models import (
    Course,
    Student,
    Enrollment
)
from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse
)

#task2 additional metadata
app=FastAPI(title='Course Management API',version='1.0',contact={
        "name": "SampathKumar",
        "email": "randompers@gmail.com"
    }
)

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return {'message':'API running'}

@app.get('/api/courses/',response_model=list[CourseResponse],tags=["Courses"])
async def get_courses(skip:int=0,limit:int=10,department_id:Optional[int]=None,db:AsyncSession=Depends(get_db)):
    q=select(Course)
    if department_id is not None:
        q=q.where(Course.department_id==department_id)
    q=q.offset(skip).limit(limit)
    r=await db.execute(q)
    return r.scalars().all()

@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="Course created successfully"
)
async def create_course(course:CourseCreate,db:AsyncSession=Depends(get_db)):
    obj=Course(**course.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

@app.get('/api/courses/{course_id}',response_model=CourseResponse)
async def get_course(course_id:int,db:AsyncSession=Depends(get_db)):
    r=await db.execute(select(Course).where(Course.id==course_id))
    obj=r.scalar_one_or_none()
    if not obj:
        raise HTTPException(404,'Course not found')
    return obj

@app.put('/api/courses/{course_id}',response_model=CourseResponse)
async def update_course(course_id:int,course:CourseUpdate,db:AsyncSession=Depends(get_db)):
    r=await db.execute(select(Course).where(Course.id==course_id))
    obj=r.scalar_one_or_none()
    if not obj:
        raise HTTPException(404,'Course not found')
    for k,v in course.model_dump(exclude_unset=True).items():
        setattr(obj,k,v)
    await db.commit()
    await db.refresh(obj)
    return obj

@app.delete('/api/courses/{course_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id:int,db:AsyncSession=Depends(get_db)):
    r=await db.execute(select(Course).where(Course.id==course_id))
    obj=r.scalar_one_or_none()
    if not obj:
        raise HTTPException(404,'Course not found')
    await db.delete(obj)
    await db.commit()
    return Response(status_code=204)

#task2 additional function 
def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")

@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(

    enrollment: EnrollmentCreate,

    background_tasks: BackgroundTasks,

    db: AsyncSession = Depends(get_db)

):

    student_result = await db.execute(
        select(Student).where(
            Student.id == enrollment.student_id
        )
    )

    student = student_result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_enrollment = Enrollment(

        student_id=enrollment.student_id,

        course_id=enrollment.course_id,

        enrollment_date=enrollment.enrollment_date,

        grade=enrollment.grade

    )

    db.add(new_enrollment)

    await db.commit()

    await db.refresh(new_enrollment)

    background_tasks.add_task(

        send_confirmation_email,

        student.email

    )

    return new_enrollment