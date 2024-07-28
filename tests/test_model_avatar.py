from lsl_gw_lib.models import Avatar
from pydantic import ValidationError
import pytest
import uuid


def test_avatar_constructor():
	u = uuid.uuid4()
	a0 = Avatar(u, 'FName LName')
	a1 = Avatar(u, 'NickName')
	a2 = Avatar(u, 'NickName Resident')
	a3 = Avatar(u, 'nickname.resident')
	a4 = Avatar(u, 'fname.lname')
	a5 = Avatar(uuid.uuid4(), 'fname.lname')
	a6 = Avatar(id=u, firstName='FName', lastName='LName')

	assert a1 == a2
	assert a0 == a4
	assert a4 != a5
	assert a0 == a6
	assert a2 == a3

def test_avatar_validator():
	with pytest.raises(ValidationError):
		Avatar(uuid.uuid4(), '12345678901234567890123456789012')
	with pytest.raises(ValidationError):
		Avatar(uuid.uuid4(), 'abc.12345678901234567890123456789012')
	with pytest.raises(ValidationError):
		Avatar(uuid.uuid4(), 'abc def 123')
