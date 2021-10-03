import datetime
import random
import typing

import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import logged_context
from cotd.static import StaticReader


@logged_context
# @functools.partial(cacheable_handler, key=datetime.datetime.utcnow().date(), path="video.file_id")
# TODO figure out how to implement this
def cringelord(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> None:
    def __cringelord_text(id: int, username: str):
        return "Cringe lord of the day" f"👑👉 <a href='tg://user?id={id}'>@{username}</a>"

    if not cache.cringelord:
        cache.cringelord = {}

    try:
        _cringelord = cache.cringelord[datetime.datetime.utcnow().date()]

        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=__cringelord_text(_cringelord.id, _cringelord.username),
        )
    except KeyError:
        _cringelord = cache.users[random.choice(list(cache.users))]

        context.dispatcher.logger.debug(_cringelord)
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=__cringelord_text(_cringelord.id, _cringelord.username),
        )

        cache.cringelord[datetime.datetime.utcnow().date()] = _cringelord

        context.dispatcher.logger.debug(
            "serving computed cringelord"
            f"\nupdated cache {datetime.datetime.utcnow().date()}:{_cringelord}"
        )
        return message
    else:
        context.dispatcher.logger.debug(f"serving from cache: {cache.cringelord}")

        return message
