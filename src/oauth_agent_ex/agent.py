from pydantic import BaseModel, Field
from uuid import uuid4
import jwt
from datetime import datetime, timedelta
from typing import Optional

class AgentIdentity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def generate_jwt(self, secret_key: str, expiration: int = 3600) -> str:
        """
        Generate a JWT for the agent.
        
        :param secret_key: Secret key for signing the JWT
        :param expiration: Token expiration time in seconds (default: 1 hour)
        :return: JWT string
        """
        payload = {
            "sub": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=expiration)
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")
    
    @staticmethod
    def validate_jwt(token: str, secret_key: str) -> dict:
        """
        Validate and decode a JWT.
        
        :param token: JWT string to validate
        :param secret_key: Secret key used for signing the JWT
        :return: Decoded payload if valid
        :raises jwt.InvalidTokenError: If the token is invalid
        """
        return jwt.decode(token, secret_key, algorithms=["HS256"])

def create_agent_identity(user_id: str, name: str) -> AgentIdentity:
    """
    Create a new AgentIdentity instance.
    
    :param user_id: ID of the user associated with this agent
    :param name: Name of the agent
    :return: AgentIdentity instance
    """
    return AgentIdentity(user_id=user_id, name=name)
