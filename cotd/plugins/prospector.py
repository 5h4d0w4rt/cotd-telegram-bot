import telegram
import telegram.ext
from cotd.cacher import MediaCache
import typing


def cache_users(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
) -> None:
    if not cache.users:
        cache.users = {}

    if not cache.users.get(update.effective_user.id):
        cache.users[update.effective_user.id] = update.effective_user

    context.dispatcher.logger.debug(cache.users)
