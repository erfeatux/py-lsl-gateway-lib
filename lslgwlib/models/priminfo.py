from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class PrimInfo(BaseModel):
    # id calculates on client side
    id: UUID
    creatorId: UUID
    name: str = Field(pattern=r"[\x20-\x7b\x7d-\x7e]{0, 63}")
    description: str = Field(pattern=r"[\x20-\x7b\x7d-\x7e]{0, 127}")
    createdAt: datetime
