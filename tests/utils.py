from random import choices


def genStr(len: int = 63, utf8: bool = False) -> str:
    rng = 0x7F
    if utf8:
        rng = 0x7FF
    return str(
        "".join(
            choices(
                "".join(tuple(chr(i) for i in range(32, rng) if chr(i).isprintable())),
                k=len,
            )
        ).encode("UTF-8")
    )
