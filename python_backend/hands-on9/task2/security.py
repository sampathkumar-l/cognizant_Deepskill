"""
Security utilities: password hashing (bcrypt, carried over from Task 1) plus
JWT creation/decoding for Task 2 (steps 91-92).

SECRET_KEY below is a placeholder for local/hands-on use only. In a real
deployment this must come from an environment variable / secrets manager and
never be committed to source control.

Reminder (step 95, "what does a JWT actually protect?"):
JWT payloads are base64url-encoded, NOT encrypted - anyone who intercepts a
token can decode and read the payload. The signature only proves the token
was issued by someone holding SECRET_KEY (i.e. it wasn't tampered with).
Never put passwords, card numbers, or other secrets inside the payload.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# --- Password hashing (bcrypt) -------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT -------------------------------------------------------------------

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "handson9-local-dev-secret-do-not-use-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Raises jose.JWTError if the token is invalid, tampered with, or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
