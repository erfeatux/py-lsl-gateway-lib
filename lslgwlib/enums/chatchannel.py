from enum import IntEnum


class ChatChannel(IntEnum):
    PUBLIC = 0  #         Chat channel that broadcasts to all nearby users
    DEBUG = 0x7FFFFFFF  # Chat channel reserved for script debugging and error messages
