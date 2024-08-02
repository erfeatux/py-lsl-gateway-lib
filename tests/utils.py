from random import choices


def genStr(len: int = 63, uft8: bool = False) -> str:
    rng = 0x7F
    if uft8:
        rng = 0x7FF
    return str(
        "".join(
            choices(
                "".join(tuple(chr(i) for i in range(32, rng) if chr(i).isprintable())),
                k=len,
            )
        ).encode("UTF-8")
    )
