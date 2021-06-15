import logging
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
        dispatcher: telegram.ext.Dispatcher = args[1].dispatcher
        dispatcher.logger.debug(args)
        dispatcher.logger.debug(kwargs)

        result = f(*args, **kwargs)
        dispatcher.logger.debug(f"{f.__name__} : {result}")

        return result

    return wrapper


def cacheable_handler(f, key: typing.Any, path: str):
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
def question_mark(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {1: "???", 2: "слыш ты ебало то завали"}

    decision = roll_map.get(random.randint(0, 10))
    if not decision:
        return None
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )


@logged_context
def no_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {0: "пидора ответ"}

    decision = roll_map.get(random.randint(0, 2))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )


@logged_context
def yes_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {0: "пизда"}

    decision = roll_map.get(random.randint(0, 2))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )


@logged_context
def stalker_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {
        1: "Ну ты выдал!",
        3: "Блин, так не смешно же.",
        6: "А поновее ничего нет?",
        9: "Ору!",
        12: "я плакал",
        15: "бугага",
        18: "ха-ха-ха",
        21: "*выдыхает через нос*",
        24: "рофл",
        27: "ржака",
        30: "спизданул как боженька",
    }

    decision = roll_map.get(random.randint(0, 35))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=decision,
    )


@logged_context
def journalism(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {
        1: "AgACAgIAAxkBAAICBmDHxJUEM9mcS_e7novL5ZHNj2ivAALzsjEbNVs4Skv_V4-J9-kWrEvGoi4AAwEAAwIAA3MAA7y2AwABHwQ",
    }
    decision = roll_map.get(random.randint(0, 1))

    if not decision:
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id, 
        photo=decision,
    )


@logged_context
def gym_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {
        0: "CgACAgQAAxkBAAICAWDHwlSbdnzRBerbl8fhV6DppkLCAALMAgACUR4UUv1ixkAlxvRIHwQ",
        3: "CgACAgIAAxkBAAICBGDHw_5wfo37SOuyP3JNgI6gig6VAALDBwACpoWJSx8qHG1cCcQMHwQ",
        6: "CgACAgIAAxkBAAICBWDHxCIPQ2aZuEk6RaAm_fCXe0DKAAIXAgAC13S5SH7Or-N7YQh4HwQ",
    }
    decision = roll_map.get(random.randint(0, 9))

    if not decision:
        return None

    return context.bot.sendAnimation(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id, 
        animation=decision,
    )


@logged_context
def leftie_meme_detector(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if len(update.message.text) < 1024:
        return None
    
    roll_map = {
        1: "опять левацкие мемы постишь...",
        3: "TL;DR",
        5: "ну и нахуя ты это высрал?",
        7: "?",
        9:"а что сказать то хотел?",
    }
    decision = roll_map.get(random.randint(0, 10))

    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )


@logged_context
def voice_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {1: True}
    decision = roll_map.get(random.randint(0, 1))

    if not decision:
        return None

    return context.bot.sendSticker(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        sticker="CAACAgIAAxkBAAIBy2DHu6uTHF_uKSwtLRuWcUmHNHejAAI-AQAC39LPAoZ3xK3gRdEhHwQ",
    )


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

    @functools.partial(cacheable_handler, key="ribnikov", path="video.file_id")
    @logged_context
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

    @functools.partial(cacheable_handler, key="sniff_dog", path="photo[0].file_id")
    @logged_context
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

    return choice_map[random.choice(["based", "cringe"])](update, context, cache=cache, data=data)


@logged_context
@functools.partial(cacheable_handler, key="oldfellow", path="video.file_id")
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
@functools.partial(cacheable_handler, key="kekw", path="video.file_id")
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
@functools.partial(cacheable_handler, key="go_away", path="video.file_id")
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
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data.ozon_secret,
    )


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
# @functools.partial(cacheable_handler, key=datetime.datetime.utcnow().date(), path="video.file_id")
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
