import functools
import random
import typing
import uuid

import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, is_reply, logged_context
from cotd.static import StaticReader
from telegram import chat


def _chance(percent: float = 0.5):
    return round(random.random(), 1) < percent


@logged_context
def oldfellow_inline(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    data: typing.Type[StaticReader],
):
    """create old fellow result in inline mode"""
    # TODO move static to cache initialization with timer
    oldfellow_cache = context.bot_data.setdefault("cache", {}).setdefault("oldfellow", None)
    if not oldfellow_cache:
        video = context.bot.send_video(chat_id=context.dispatcher._cotd_db, video=data.oldfellow)
        context.bot.delete_message(video.chat_id, video.message_id)
        context.bot_data["cache"]["oldfellow"] = video.video.file_id
    context.dispatcher.logger.debug(context.bot_data)
    return telegram.InlineQueryResultCachedVideo(
        id=str(uuid.uuid4()),
        title="oldfellow",
        video_file_id=context.bot_data["cache"]["oldfellow"],
    )


@logged_context
@functools.partial(cacheable_handler, key="kekw", path="video.file_id")
def kekw(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    if not is_reply(update):
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=cache.kekw or data.kekw,
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
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    if not is_reply(update):
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
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data.ozon_secret,
    )


@logged_context
def dump(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    _tmpl = "{:<8} {:<15} {:<10}"

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=data.ozon_secret,
    )


@logged_context
def leftie_meme_detector(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance():
        return None

    if len(update.message.text) < 1024:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "опять левацкие мемы постишь...",
                "Разумеется, на приведённое выше рассуждение есть что возразить. Но назвать сказанное идиотизмом всё-таки нельзя: это вполне корректно выстроенная модель.",
                "ну и нахуя ты это высрал?",
                "?",
                "а что сказать то хотел?",
                "интересное чтиво",
                "TL;DR",
                "don't care + didn't ask + L + Ratio + you fell of + cancelled + quote retweet + you're white + suck on deez nuts + caught in 4k + soyjak + cry about it + delete this + cope + seethe + cringe + ok boomer + incel + virgin + Karen + you're not just a clown you're the entire circus + go touch some grass",
                "Кремль взбешен, но что делать — пока не знает",
            ]
        ),
    )


@logged_context
def bot_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.15):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "что хотел?",
                "а что опять я то?",
                "пошёл нахуй",
                "я и так пашу без отдыха, а тут ты ещё",
            ]
        ),
    )

logged_context
def patriot_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.5):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "Побольше бы таких новостей!",
                "РОССИЯ🇷🇺РОССИЯ🇷🇺РОССИЯ",
            ]
        ),
    )


@logged_context
def question_mark(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.3):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "???",
                "слыш ты ебало то завали",
                "ты сейчас быканул или мне показалось?",
            ]
        ),
    )


@logged_context
def no_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.35):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="пидора ответ",
    )


@logged_context
def yes_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.35):
        return None

    reaction_text = "пизда"

    if _chance(0.3):
        reaction_text = "1/5, чел"

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=reaction_text,
    )


def massacre_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="🍉",
    )


def trista_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.3):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="отсоси у тракториста",
    )


@logged_context
def pig_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance():
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "🐷",
                "🐽",
                "🐖",
            ]
        ),
    )


@logged_context
def watermelon_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="🔪",
    )


@logged_context
@functools.partial(cacheable_handler, key="stuffy", path="photo[0].file_id")
def stuffy_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.4):
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.stuffy or data.stuffy,
    )


@logged_context
@functools.partial(cacheable_handler, key="music", path="photo[0].file_id")
def music_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:
    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.music or data.music,
    )


@logged_context
@functools.partial(cacheable_handler, key="journalism", path="photo[0].file_id")
def journalism_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:

    if not _chance(0.4):
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.journalism or data.journalism,
    )


@logged_context
def gym_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not _chance():
        return None

    return context.bot.send_animation(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        animation=random.choice(
            [
                "CgACAgQAAxkBAAICAWDHwlSbdnzRBerbl8fhV6DppkLCAALMAgACUR4UUv1ixkAlxvRIHwQ",
                "CgACAgIAAxkBAAICBGDHw_5wfo37SOuyP3JNgI6gig6VAALDBwACpoWJSx8qHG1cCcQMHwQ",
                "CgACAgIAAxkBAAICBWDHxCIPQ2aZuEk6RaAm_fCXe0DKAAIXAgAC13S5SH7Or-N7YQh4HwQ",
            ]
        ),
    )
