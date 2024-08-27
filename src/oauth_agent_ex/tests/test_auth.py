import pytest
from oauth_aci.auth import AgentAuthorizationCodeFlow, AgentClientCredentialsFlow
from oauth_aci.agent import create_agent_identity
from oauth_aci.exceptions import InvalidAgentToken, UnauthorizedAgent

@pytest.mark.asyncio
async def test_agent_authorization_code_flow():
    flow = AgentAuthorizationCodeFlow("client_id", "client_secret")
    agent = create_agent_identity("user123", "TestAgent")
    
    # Test valid authorization code
    token = await flow.fetch_token(agent, "valid_code")
    assert token.access_token is not None

    # Test invalid authorization code
    with pytest.raises(InvalidAgentToken):
        await flow.fetch_token(agent, "invalid_code")

@pytest.mark.asyncio
async def test_agent_client_credentials_flow():
    flow = AgentClientCredentialsFlow("client_id", "client_secret")
    agent = create_agent_identity("valid_user", "TestAgent")
    
    # Test valid client credentials
    token = await flow.fetch_token(agent)
    assert token.access_token is not None

    # Test invalid client credentials
    invalid_agent = create_agent_identity("invalid_user", "TestAgent")
    with pytest.raises(UnauthorizedAgent):
        await flow.fetch_token(invalid_agent)
