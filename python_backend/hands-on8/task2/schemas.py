

from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict



class DepartmentBase(BaseModel):
    name: str
    head_of_dept: Optional[str] = None
    budget: Optional[float] = 0.0


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CoursePatch(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None
    enrollment_year: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
