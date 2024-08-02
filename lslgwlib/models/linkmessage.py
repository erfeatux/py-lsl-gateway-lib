from pydantic import BaseModel, Field, AliasChoices, field_validator
from uuid import UUID


from lslgwlib.enums import LinkNum


class LinkMessage(BaseModel):
    prim: int = Field(
        default=LinkNum.THIS,
        ge=LinkNum.THIS,
        le=255,
        validation_alias=AliasChoices(
            "prim", "prim_num", "sender", "source", "from", "target", "to"
        ),
    )
    num: int = Field(default=0, ge=-0x80000000, le=0x7FFFFFFF)
    string: str = Field(default="", validation_alias=AliasChoices("string", "str"))
    id: str | UUID = Field(default="")

    @field_validator("id")
    def id_validator(cls, id: str | UUID) -> str | UUID:
        if isinstance(id, UUID):
            return id
        try:
            uuid = UUID(id)
        except Exception:
            return id
        else:
            return uuid
