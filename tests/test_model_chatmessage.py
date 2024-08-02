from lslgwlib.models import ChatMessage
from pydantic import ValidationError
from tests.utils import genStr
import pytest


def test_chatmessage_validator():
    with pytest.raises(ValueError):
        ChatMessage(name=genStr(), msg=genStr(len=1024, uft8=True))
    with pytest.raises(ValidationError):
        ChatMessage(name=genStr(), msg=genStr(len=1025))
