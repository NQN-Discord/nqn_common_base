from enum import IntEnum, auto


class GuildStateUpdateEvent(IntEnum):
    guild_update = auto()
    role_set = auto()
    role_delete = auto()
    channel_set = auto()
    channel_delete = auto()
    emojis_set = auto()
    member_update = auto()
