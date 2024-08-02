from lslgwlib.models import LinkMessage
from pydantic import ValidationError
from uuid import UUID
import pytest


def test_linkmessage_validator():
    with pytest.raises(ValidationError):
        LinkMessage(num=-0x80000001)
    with pytest.raises(ValidationError):
        LinkMessage(num=0x80000000)
    with pytest.raises(ValidationError):
        LinkMessage(str=0)
    with pytest.raises(ValidationError):
        LinkMessage(id=0)
    assert isinstance(LinkMessage(id="00000000-0000-0000-0000-000000000000").id, UUID)
