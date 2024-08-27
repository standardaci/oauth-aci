class AgentAuthError(Exception):
    """Base exception for agent authentication errors."""

class InvalidAgentToken(AgentAuthError):
    """Raised when an agent token is invalid."""

class UnauthorizedAgent(AgentAuthError):
    """Raised when an agent is not authorized to perform an action."""

class AgentNotFound(AgentAuthError):
    """Raised when an agent is not found."""

class InvalidScope(AgentAuthError):
    """Raised when an invalid scope is requested or used."""
