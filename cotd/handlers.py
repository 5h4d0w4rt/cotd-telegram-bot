import telegram
import telegram.ext
import random
import typing
import datetime
import functools
from cotd.cacher import MediaCache
from cotd.static import Static


def logged_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        context: telegram.ext.CallbackContext = args[1]
        context.dispatcher.logger.debug(args)
        context.dispatcher.logger.debug(kwargs)

        result = f(*args, **kwargs)
        context.dispatcher.logger.debug(f'{f.__name__} : {result}')

        return result

    return wrapper


def cacheable_context(f, key: typing.Any, path: str):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):

        if "cache" not in kwargs:
            return f(*args, **kwargs)

        cache = kwargs["cache"]
        result = f(*args, **kwargs)
        if not cache.key:
            setattr(cache, key, functools.reduce(getattr, path.split("."), result))

        return result

    return wrapper


def _is_reply(update: telegram.Update):

    try:
        update.message.reply_to_message.message_id
    except AttributeError:
        return False
    else:
        return True


def start(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text="hi")


@logged_context
def iscringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
) -> telegram.Message:

    if not _is_reply(update):
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Can"t see cringe though, reply to a cringe post',
        )

    @functools.partial(cacheable_context, key="ribnikov", path="video.file_id")
    def _process_based(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
        cache: typing.Type[MediaCache] = None,
        data: typing.Type[Static] = None,
    ) -> telegram.Message:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=cache.ribnikov or data.ribnikov,
        )

    @functools.partial(cacheable_context, key="sniff_dog", path=".photo[0].file_id")
    def _process_cringe(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
        cache: typing.Type[MediaCache] = None,
        data: typing.Type[Static] = None,
    ) -> telegram.Message:
        return context.bot.send_photo(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            photo=cache.sniff_dog or data.sniff_dog,
        )

    choice_map = {"based": _process_based, "cringe": _process_cringe}

    return choice_map[random.choice(["based", "cringe"])](
        update=update, context=context, cache=cache, data=data
    )


@logged_context
@functools.partial(cacheable_context, key="oldfellow", path="video.file_id")
def oldfellow(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
) -> telegram.Message:

    if not _is_reply(update):
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=cache.oldfellow or data.oldfellow,
        )
    return context.bot.send_video(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.reply_to_message.message_id,
        video=cache.oldfellow or data.oldfellow,
    )


@logged_context
@functools.partial(cacheable_context, key="kekw", path="video.file_id")
def kekw(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
) -> telegram.Message:

    if not _is_reply(update):
        return context.bot.send_video(
            chat_id=update.effective_chat.id, video=cache.kekw or data.kekw
        )

    return context.bot.send_video(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.reply_to_message.message_id,
        video=cache.kekw or data.kekw,
    )


@logged_context
@functools.partial(cacheable_context, key="go_away", path="video.file_id")
def goaway(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
) -> telegram.Message:

    if not _is_reply(update):
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=cache.go_away or data.go_away,
        )
    return context.bot.send_video(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.reply_to_message.message_id,
        video=cache.go_away or data.go_away,
    )


@logged_context
def secret(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    data: typing.Type[Static] = None,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text=data.ozon_secret)


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


@logged_context
# @functools.partial(cacheable_context, key=datetime.datetime.utcnow().date(), path="video.file_id")
# TODO figure out how to implement this
def cringelord(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
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


# TODO pre-process/post-process handlers to simplify logic
# TODO cacheable decorator
# TODO storage: github private repo
# TODO cringe_poster_factor = rate(cringe posts(those marked by cringe bot) / all posts)
# to determine cringelord of the day
# store all cringelords of the day in a list
# and store all cringeposts in a list
# make histogram out of data
