from logging import getLogger
from typing import Optional

from discord import ClientUser, Client
from discord.http import Route

from .patch_dpy import patch_ratelimit

log = getLogger(__name__)


async def connect(
    bot: Client,
    proxy: Optional[str],
    token: str,
):
    log.info("Logging into Discord")
    if proxy is not None:
        Route.BASE = f"http://{proxy}/api/v8"

    if token.startswith("Basic "):
        token = token.replace("Basic ", "")
        log.warning("TOKEN USING BASIC AUTH")
    await bot.login(token=token)
    patch_ratelimit()

    app_info = await bot.application_info()
    if app_info.team:
        bot.owner = app_info.team.owner
    else:
        bot.owner = app_info.owner
    log.info(f"Owned by: {bot.owner}")
