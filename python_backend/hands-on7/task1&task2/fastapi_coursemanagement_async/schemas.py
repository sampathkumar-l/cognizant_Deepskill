from typing import Optional,List
from pydantic import BaseModel

class CourseCreate(BaseModel):
    name:str
    code:str
    credits:int
    department_id:int

class CourseUpdate(BaseModel):
    name:Optional[str]=None
    code:Optional[str]=None
    credits:Optional[int]=None
    department_id:Optional[int]=None

class CourseResponse(CourseCreate):
    id:int
    class Config:
        from_attributes=True

class StudentResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:str
    enrollment_year:int
    department_id:int
    class Config:
        from_attributes=True

class EnrollmentCreate(BaseModel):

    student_id: int

    course_id: int

    enrollment_date: str

    grade: str | None = None


class EnrollmentResponse(EnrollmentCreate):

    id: int

    class Config:

        from_attributes = True
