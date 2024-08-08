from lslgwlib.models import Invetory, InvetoryItem, Permissions
from lslgwlib.enums import InvetoryType
from pydantic import ValidationError
from copy import copy
import pytest
import re

from tests.utils import genStr


class InvetoryTestData:
    id: str
    type: str
    name: str
    description: str
    creatorId: str
    permissions: list[str]
    acquireTime: str

    def __init__(self, data: str):
        args = data.split("¦")
        if len(args) != 11:
            raise ValueError
        self.id = args[0]
        self.type = args[1]
        self.name = args[2]
        self.description = args[3]
        self.creatorId = args[4]
        self.permissions = args[5:10]
        self.acquireTime = args[10]


def test_inentory_item_model():
    td = InvetoryTestData(
        "fd42e87a-44d8-1343-9ecd-fc7dd23f6765¦7¦A&Y Re-delivery issue"
        + "¦2023-03-03 21:17:52 note card¦bf1d107f-2c7a-4e0b-9cac-d2b30ccd2821"
        + "¦581632¦581632¦0¦0¦581632¦2024-08-07T00:32:31Z"
    )
    item = InvetoryItem(
        id=td.id,
        type=td.type,
        name=td.name,
        description=td.description,
        creatorId=td.creatorId,
        permissions=Permissions(*td.permissions),
        acquireTime=td.acquireTime,
    )

    assert str(item.id) == td.id
    assert item.type == InvetoryType.NOTECARD
    assert item.name == td.name
    assert item.description == td.description
    assert str(item.creatorId) == td.creatorId
    assert item.permissions.base.ALL
    assert item.permissions.owner.MODIFY
    assert not item.permissions.group.COPY
    assert not item.permissions.everyone.TRANSFER
    assert item.permissions.next.MOVE

    tdc = copy(td)
    td.type = "8"
    with pytest.raises(ValidationError):
        item = InvetoryItem(
            id=td.id,
            type=td.type,
            name=td.name,
            description=td.description,
            creatorId=td.creatorId,
            permissions=Permissions(*td.permissions),
            acquireTime=td.acquireTime,
        )

    td = copy(tdc)
    td.name = genStr(utf8=True)
    with pytest.raises(ValidationError):
        item = InvetoryItem(
            id=td.id,
            type=td.type,
            name=td.name,
            description=td.description,
            creatorId=td.creatorId,
            permissions=Permissions(*td.permissions),
            acquireTime=td.acquireTime,
        )

    td = copy(tdc)
    td.description = genStr(256)
    with pytest.raises(ValidationError):
        item = InvetoryItem(
            id=td.id,
            type=td.type,
            name=td.name,
            description=td.description,
            creatorId=td.creatorId,
            permissions=Permissions(*td.permissions),
            acquireTime=td.acquireTime,
        )

    td = copy(tdc)
    td.permissions = ["-1", "0", "0", "0", "0"]
    with pytest.raises(ValidationError):
        item = InvetoryItem(
            id=td.id,
            type=td.type,
            name=td.name,
            description=td.description,
            creatorId=td.creatorId,
            permissions=Permissions(*td.permissions),
            acquireTime=td.acquireTime,
        )


def test_inventory_model():
    lines = [
        "fd42e87a-44d8-1343-9ecd-fc7dd23f6765¦7¦A&Y Re-delivery issue"
        + "¦2023-03-03 21:17:52 note card¦bf1d107f-2c7a-4e0b-9cac-d2b30ccd2821"
        + "¦581632¦581632¦0¦0¦581632¦2024-08-07T00:32:31Z",
        "488c4978-99e3-449a-4c98-5fc221e5a7a5¦0¦A&Y_logo¦(No Description)"
        + "¦0c2566cd-2ac9-4566-bab4-a3c4bfce58bd¦581632¦581632¦0¦0¦581632¦2024-08-07T00:32:43Z",
        "0c13f3e7-7d41-5675-ee70-fa9309319f07¦7¦New Note¦2022-05-30 19:59:13 note card"
        + "¦07ce6a4a-b34e-4e62-96e3-16f2a8b19c89¦2147483647¦2147483647¦0¦0¦581632¦2024-08-07T00:32:31Z",
        "00cc5bf5-2e03-8cfa-3c36-fc5b40238d7f¦10¦New Script¦2024-08-07 03:42:12 lsl2 script"
        + "¦07ce6a4a-b34e-4e62-96e3-16f2a8b19c89¦2147483647¦2147483647¦0¦0¦532480¦2024-08-06T23:42:12Z",
    ]

    items = list()
    for td in map(lambda x: InvetoryTestData(x), lines):
        items.append(
            InvetoryItem(
                id=td.id,
                type=td.type,
                name=td.name,
                description=td.description,
                creatorId=td.creatorId,
                permissions=Permissions(*td.permissions),
                acquireTime=td.acquireTime,
            )
        )

    inv = Invetory(items=items)
    assert len(inv.items) == 4
    assert (
        str(inv.byName("A&Y Re-delivery issue").id)
        == "fd42e87a-44d8-1343-9ecd-fc7dd23f6765"
    )
    assert len(inv.byType([InvetoryType.ANY])) == 4
    assert len(inv.byType([InvetoryType.NOTECARD])) == 2
    textures = inv.byType([InvetoryType.TEXTURE])
    assert len(textures) == 1
    assert inv.textures == textures
    assert inv.scripts[0].name == "New Script"

    assert len(inv.byNamePattern("A&Y")) == 2

    assert inv.byNamePattern(re.compile(r"^New\s\w{6}"))[0].type == InvetoryType.SCRIPT

    with pytest.raises(ValidationError):
        Invetory(items=items, filtered=InvetoryType.NOTECARD)

    with pytest.raises(ValidationError):
        Invetory(items=inv.scripts, filtered=InvetoryType.TEXTURE)
    scripts = Invetory(items=inv.scripts, filtered=InvetoryType.SCRIPT)

    with pytest.raises(ValueError):
        scripts.materials
