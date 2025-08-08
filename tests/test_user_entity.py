import pytest
from entities.user import User

def test_user_creation():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"
    assert user.id is None  # Not persisted yet

def test_user_email_unique():
    user1 = User(email="unique@example.com")
    user2 = User(email="unique@example.com")
    assert user1.email == user2.email
