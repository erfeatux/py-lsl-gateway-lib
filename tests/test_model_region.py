from lslgwlib.models import Region
from pydantic import ValidationError
import pytest


def test_region_constructor():
	assert Region('Region name (256, 512)') == Region(' Region name( 256,512 )')

def test_region_validator():
	with pytest.raises(ValidationError):
		Region('Invalid region name is (256, 512)')
	with pytest.raises(ValidationError):
		Region('Invalid region location (128, 512)')
	with pytest.raises(ValidationError):
		Region('Invalid region location (256, 511)')
