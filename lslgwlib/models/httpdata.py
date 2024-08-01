from pydantic import BaseModel, Field
from uuid import UUID

from .avatar import Avatar
from .region import Region


class HTTPData(BaseModel):
    # info from X-SecondLife-* headers:
    objectKey: UUID
    objectName: str = Field(pattern=r"[\x20-\x7b\x7d-\x7e]{0, 63}")
    owner: Avatar
    position: tuple[float, float, float]
    rotation: tuple[float, float, float, float]
    velocity: tuple[float, float, float]
    region: Region
    production: bool

    # response (different by API methods)
    data: BaseModel | list[BaseModel] | int | float | str | UUID
    # other http headers
    headers: dict[str, str]
