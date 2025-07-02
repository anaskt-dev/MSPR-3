import auth
import pytest

def test_password_hash():
    password = "testpassword123"
    hashed = auth.get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password 