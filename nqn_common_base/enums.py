from enum import IntFlag, auto


class GuildStateUpdateType(IntFlag):
    metadata = auto()
    roles = auto()
    channels = auto()
    emojis = auto()
    member = auto()


GUILD_STATE_UPDATE_ALL = (
    GuildStateUpdateType.metadata |
    GuildStateUpdateType.roles |
    GuildStateUpdateType.channels |
    GuildStateUpdateType.emojis |
    GuildStateUpdateType.member
)

# Guild update events don't contain channels or members
GUILD_UPDATE_EVENT = GUILD_STATE_UPDATE_ALL & ~GuildStateUpdateType.channels & ~GuildStateUpdateType.member
