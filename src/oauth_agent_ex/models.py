from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .utils import parse_scopes, merge_scopes, is_token_expired, generate_jwt_token, verify_jwt_token

class Scope(BaseModel):
    name: str
    description: str

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime
    refresh_token: Optional[str] = None
    scopes: List[Scope] = Field(default_factory=list)

    @property
    def scope_string(self) -> str:
        return merge_scopes([scope.name for scope in self.scopes])

    @classmethod
    def from_scope_string(cls, scope_string: str, **kwargs):
        scope_names = parse_scopes(scope_string)
        scopes = [Scope(name=name, description="") for name in scope_names]
        return cls(scopes=scopes, **kwargs)

    def is_expired(self) -> bool:
        return is_token_expired(self.expires_at)

    def to_jwt(self, secret_key: str) -> str:
        payload = {
            "sub": self.access_token,
            "scopes": self.scope_string,
            "exp": self.expires_at
        }
        return generate_jwt_token(payload, secret_key)

    @classmethod
    def from_jwt(cls, jwt_token: str, secret_key: str):
        payload = verify_jwt_token(jwt_token, secret_key)
        return cls(
            access_token=payload["sub"],
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            scopes=cls.from_scope_string(payload["scopes"]).scopes
        )

class AgentCredentials(BaseModel):
    client_id: str
    client_secret: str

    def hash_secret(self):
        self.client_secret = hash_secret(self.client_secret)

    def verify_secret(self, plain_secret: str) -> bool:
        return verify_secret(plain_secret, self.client_secret)
