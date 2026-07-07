"""
Password hashing utilities (Hands-On 9 / Task 1, step 87).

Why bcrypt and not MD5 / SHA-256 for passwords:
  - MD5 and SHA-256 are general-purpose, cryptographic *fast* hash functions -
    built for speed, which is exactly the wrong property for password storage.
    A modern GPU can compute billions of SHA-256 hashes per second, so a
    stolen hash-and-salt database can be brute-forced very quickly.
  - bcrypt is a *deliberately slow*, adaptive hash function with a tunable
    "work factor" (cost). Each increment of the cost roughly doubles the time
    needed per hash, so as hardware gets faster you raise the cost and the
    attack stays expensive. It also generates and stores a random salt for
    you automatically, so identical passwords never produce identical hashes.
  - This is why passlib's CryptContext(schemes=["bcrypt"]) is used below
    instead of hashlib.sha256(password).hexdigest().
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plain-text password with bcrypt. Returns only the hash -
    the plain-text value is never stored or logged anywhere."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain-text password against a stored bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)
