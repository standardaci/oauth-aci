import pytest
from oauth_aci.utils import generate_secure_random_string, is_token_expired
from datetime import datetime, timedelta

def test_generate_secure_random_string():
    # Test default length
    string1 = generate_secure_random_string()
    assert len(string1) == 32
    
    # Test custom length
    string2 = generate_secure_random_string(length=64)
    assert len(string2) == 64
    
    # Test uniqueness
    string3 = generate_secure_random_string()
    assert string1 != string2 != string3
    
    # Test character set
    assert all(c.isalnum() for c in string1)

@pytest.mark.parametrize("delta,expected", [
    (timedelta(seconds=-1), True),   # Expired
    (timedelta(seconds=1), False),   # Not expired
    (timedelta(0), False),           # Edge case: expiring now
])
def test_is_token_expired(delta, expected):
    now = datetime.utcnow()
    expires_at = now + delta
    assert is_token_expired(expires_at) == expected

def test_is_token_expired_with_timezone():
    from datetime import timezone
    
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=1)
    assert not is_token_expired(expires_at)
    
    expires_at = now - timedelta(hours=1)
    assert is_token_expired(expires_at)
