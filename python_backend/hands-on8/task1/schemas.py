from typing import Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr


# -----------------------------
# Department Schemas
# -----------------------------

class DepartmentBase(BaseModel):
    name: str
    head_of_dept: str
    budget: float


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    head_of_dept: Optional[str] = None
    budget: Optional[float] = None


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# Course Schemas
# -----------------------------

class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# Student Schemas
# -----------------------------

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    enrollment_year: int
    department_id: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_year: Optional[int] = None
    department_id: Optional[int] = None


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# Enrollment Schemas
# -----------------------------

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[str] = None


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None


class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True


# -----------------------------
# Nested Response
# -----------------------------

class DepartmentWithCourses(DepartmentResponse):
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True