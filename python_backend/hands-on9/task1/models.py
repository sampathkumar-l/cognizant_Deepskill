"""
User model.

IMPORTANT: only `hashed_password` is ever persisted. The plain-text password
that arrives in a request is used once (to compute the hash) and then
discarded - it is never written to this table, never logged, and never
returned in a response (see schemas.UserResponse, which deliberately omits it).
"""

from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
