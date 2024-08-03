from lslgwlib.models import Touch, Avatar
from pydantic import ValidationError
from uuid import uuid4
import pytest


def test_touch_validator():
    touch = Touch(
        prim=0,
        avatar=Avatar(uuid4(), "Test Name"),
        startST=(0.1, 0.5),
        endST=(0.2, 0.9),
        startUV=(0.11, 0.55),
        endUV=(0.22, 0.99),
    )
    assert touch.prim == 0
    assert touch.startST == (0.1, 0.5)
    assert touch.endST == (0.2, 0.9)
    assert touch.startUV == (0.11, 0.55)
    assert touch.endUV == (0.22, 0.99)

    with pytest.raises(ValidationError):
        Touch(
            prim=256,
            avatar=Avatar(uuid4(), "Test Name"),
            startST=(0.1, 0.5),
            endST=(0.2, 0.9),
            startUV=(0.11, 0.55),
            endUV=(0.22, 0.99),
        )

    with pytest.raises(ValidationError):
        Touch(
            prim=1,
            avatar=Avatar(uuid4(), "Test Name Invalid"),
            startST=(0.1, 0.5),
            endST=(0.2, 0.9),
            startUV=(0.11, 0.55),
            endUV=(0.22, 0.99),
        )

    with pytest.raises(ValidationError):
        Touch(
            prim=1,
            avatar=Avatar(uuid4(), "Test Name"),
            startST=(-0.1, 0.5),
            endST=(0.2, 0.9),
            startUV=(0.11, 0.55),
            endUV=(0.22, 0.99),
        )

    with pytest.raises(ValidationError):
        Touch(
            prim=1,
            avatar=Avatar(uuid4(), "Test Name"),
            startST=(0.1, 0.5),
            endST=(0.2, 0.9),
            startUV=(0.11, 0.55),
            endUV=(0.22, 1.99),
        )
