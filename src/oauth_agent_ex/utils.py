import secrets
import string
from datetime import datetime, timezone
from typing import List, Dict
import jwt
import bcrypt
from datetime import timedelta

def generate_secure_random_string(length: int = 32, include_special_chars: bool = False) -> str:
    alphabet = string.ascii_letters + string.digits
    if include_special_chars:
        alphabet += string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def is_token_expired(expires_at: datetime) -> bool:
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return now > expires_at

def generate_agent_id() -> str:
    return f"agent_{generate_secure_random_string(16)}"

def parse_scopes(scope_string: str) -> List[str]:
    return scope_string.split()

def merge_scopes(scopes: List[str]) -> str:
    return " ".join(scopes)

def validate_scope(required_scope: str, granted_scopes: List[str]) -> bool:
    return required_scope in granted_scopes

def generate_jwt_token(payload: Dict, secret_key: str, expiration: int = 3600) -> str:
    payload['exp'] = datetime.utcnow() + timedelta(seconds=expiration)
    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_jwt_token(token: str, secret_key: str) -> Dict:
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")

def hash_secret(secret: str) -> str:
    return bcrypt.hashpw(secret.encode(), bcrypt.gensalt()).decode()

def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    return bcrypt.checkpw(plain_secret.encode(), hashed_secret.encode())
