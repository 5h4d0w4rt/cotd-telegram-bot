import functools
import random
import typing
import uuid
import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, is_reply, logged_context
from cotd.static import StaticReader


def oldfellow_inline_impl(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
):
    """create old fellow result in inline mode"""
    return telegram.InlineQueryResultCachedVideo(
        id=str(uuid.uuid4()),
        title="oldfellow",
        # TODO: make this reliable by adding database with cached files
        video_file_id="BAACAgIAAx0EWzXwBwACAQNhXIIZ6wX4ji5nZIf6g1Q7nBOw3gACZxEAAsFp4Upg6GrkPvVSfCEE",
    )


@logged_context
@functools.partial(cacheable_handler, key="oldfellow", path="video.file_id")
def oldfellow(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    if not is_reply(update):
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
def leftie_meme_detector(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if len(update.message.text) < 1024:
        return None

    roll_map = {
        1: "опять левацкие мемы постишь...",
        3: "Разумеется, на приведённое выше рассуждение есть что возразить. Но назвать сказанное идиотизмом всё-таки нельзя: это вполне корректно выстроенная модель.",
        5: "ну и нахуя ты это высрал?",
        7: "?",
        9: "а что сказать то хотел?",
        12: "интересное чтиво",
        14: "TL;DR",
    }
    decision = roll_map.get(random.randint(0, 16))

    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )


@logged_context
def question_mark(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    roll_map = {
        1: "???",
        2: "слыш ты ебало то завали",
        3: "ты сейчас быканул или мне показалось?",
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
def no_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 5) != 3:
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
    if random.randint(0, 5) != 3:
        return None

    reaction_text = "пизда"

    if random.randint(0, 5) == 3:
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
    if random.randint(0, 1) == 0:
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
    roll_map = {
        1: "🐷",
        2: "🐽",
        3: "🐖",
    }

    decision = roll_map.get(random.randint(0, 5))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
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
    if random.randint(0, 5) != 3:
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
    if random.randint(0, 5) != 3:
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
    roll_map = {
        0: "CgACAgQAAxkBAAICAWDHwlSbdnzRBerbl8fhV6DppkLCAALMAgACUR4UUv1ixkAlxvRIHwQ",
        3: "CgACAgIAAxkBAAICBGDHw_5wfo37SOuyP3JNgI6gig6VAALDBwACpoWJSx8qHG1cCcQMHwQ",
        6: "CgACAgIAAxkBAAICBWDHxCIPQ2aZuEk6RaAm_fCXe0DKAAIXAgAC13S5SH7Or-N7YQh4HwQ",
    }
    decision = roll_map.get(random.randint(0, 9))

    if not decision:
        return None

    return context.bot.send_animation(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        animation=decision,
    )
