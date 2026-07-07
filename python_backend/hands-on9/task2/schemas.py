from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field


# ---------------------------------------------------------------- Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# ---------------------------------------------------------------- Department
class DepartmentCreate(BaseModel):
    name: str
    head_of_dept: Optional[str] = None
    budget: Optional[float] = 0.0


class DepartmentResponse(DepartmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------- Course
class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseResponse(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------------------------------------------------------------- Errors
class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
