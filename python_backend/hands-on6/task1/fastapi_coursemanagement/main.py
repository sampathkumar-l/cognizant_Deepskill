from fastapi import FastAPI
from schemes import (
    CourseCreate,
    CourseResponse
)

app = FastAPI(
    title="Course Management API",
    version="1.0"
)

courses = []


@app.get("/")
async def root():
    return {
        "message": "API running"
    }


@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=201
)
async def create_course(course: CourseCreate):

    new_course = {
        "id": len(courses) + 1,
        **course.model_dump()
    }

    courses.append(new_course)

    return new_course

@app.get(
    "/api/courses/",
    response_model=list[CourseResponse]
)
async def get_courses():
    return courses