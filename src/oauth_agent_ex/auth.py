from abc import ABC, abstractmethod
from .agent import AgentIdentity
from .models import Token, Scope
from .exceptions import InvalidAgentToken, UnauthorizedAgent
from datetime import datetime, timedelta
import jwt

class BaseOAuthFlow(ABC):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    async def fetch_token(self, agent: AgentIdentity) -> Token:
        pass

class AgentAuthorizationCodeFlow(BaseOAuthFlow):
    async def fetch_token(self, agent: AgentIdentity, authorization_code: str) -> Token:
        # Simulate token exchange using the authorization code
        if not self.validate_authorization_code(authorization_code):
            raise InvalidAgentToken("Invalid authorization code.")
        
        # Generate a new token
        token = self.issue_token(agent)
        return token

    def validate_authorization_code(self, code: str) -> bool:
        # Placeholder for actual validation logic
        return code == "valid_code"

    def issue_token(self, agent: AgentIdentity) -> Token:
        expiration = datetime.utcnow() + timedelta(hours=1)
        access_token = agent.generate_jwt(secret_key="your_secret_key", expiration=3600)
        return Token(access_token=access_token, expires_at=expiration)

class AgentClientCredentialsFlow(BaseOAuthFlow):
    async def fetch_token(self, agent: AgentIdentity) -> Token:
        # Validate client credentials (this is a placeholder)
        if agent.user_id != "valid_user":
            raise UnauthorizedAgent("Invalid client credentials.")
        
        # Generate a new token
        token = self.issue_token(agent)
        return token

    def issue_token(self, agent: AgentIdentity) -> Token:
        expiration = datetime.utcnow() + timedelta(hours=1)
        access_token = agent.generate_jwt(secret_key="your_secret_key", expiration=3600)
        return Token(access_token=access_token, expires_at=expiration)

async def validate_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
