from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserRegister(BaseModel):
    """Incoming registration payload. Plain-text password lives only here,
    for the single moment between request parsing and hashing."""
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")


class UserResponse(BaseModel):
    """Response payload - notice hashed_password is NOT included.
    An API should never echo back password material, hashed or otherwise."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
