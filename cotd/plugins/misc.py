import functools
import random
import typing
import uuid

import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, is_reply, logged_context, check_chance
from cotd.static import StaticReader


def _to_code_block(text):
    return f"<code>{text}</code>"


@logged_context
@functools.partial(cacheable_handler, key="sf", path="photo[0].file_id")
def cuno_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 1) != 0:
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.sf or data.sf,
    )


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
def leftie_meme_detector(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance():
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
@functools.partial(cacheable_handler, key="journalism", path="photo[0].file_id")
def journalism_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(0.4):
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.journalism or data.journalism,
    )


@logged_context
def patriot_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(1):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=random.choice(
            [
                "Побольше бы таких новостей!",
                "Живи в избе - ешь ежа",
                "РОССИЯ🇷🇺РОССИЯ🇷🇺РОССИЯ",
                "так победим!",
            ]
        ),
    )


@logged_context
def bot_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if check_chance(0.3):
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            video="BAACAgIAAx0EWzXwBwACC1diUGH6jS-O48JTmpEtjHS-HxS3aAACWhkAAm4pgUox7IuFDlfzkiME",
            reply_to_message_id=update.message.message_id,
        )

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


@logged_context
def question_mark(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(0.3):
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

    if not check_chance(0.35):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="пидора ответ",
    )


@logged_context
def grass_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(0.35):
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="бро, пойди потрогай траву",
    )


@logged_context
def yes_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(0.35):
        return None

    reaction_text = "пизда"

    if check_chance(0.3):
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


@logged_context
def tweet_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    stuff_twitter_retard_says = [
        ">ORYX SAYS",
        ">CONFIRMED BY VISUAL EVIDENCE",
        ">AUDIO REPORTS DETAIL",
        ">UKRANIAN MEDIA REPORTS",
        ">PENTAGON PROJECTS",
        ">U.K. SPY CHIEF INFORMS",
        ">UNCONFIRMED BUT REALISTIC REPORTS",
        ">ACCORDING TO ANALYSTS",
        ">THE UKRANIAN SECURITY SERVICE HAS ANNOUNCED",
        ">UKRANIAN INTELLIGENCE CLAIM",
        ">BELLINCUNT CONFIRMS",
        ">RUSSIAN (((DISSIDENT))) PREDICTS",
        ">PUBLIC SENTIMENT SUGGESTS",
        ">MULTIPLE REPORTS FROM BOTH SIDES",
        ">UNNAMED SOURCES CITED",
        ">ACCORDING TO UNNAMED (((WESTERN))) OFFICIALS",
        ">CITING UNNAMED WESTERN OFFICIALS",
        ">A SOURCE FAMILIAR WITH RUSSIAN THINKING",
        ">A SOURCE WHO SPOKE ON CONDITION OF ANONYMITY",
        ">US INTELLIGENCE REVEALS",
        ">UK INTELLIGENCE CONFIRMS",
        ">NEXTA SAYS",
        ">REUTERS SAYS",
        ">/K/ TOLD ME",
        ">I MADE IT UP",
        ">US OFFICIALS SAY",
        ">PENTAGON SAYS",
        ">DOD BELIEVES",
        ">GENERAL MILLEY CONFIRMS",
        ">FBI AGREES",
        ">DIPLOMATS SURMISE",
        ">EU PROMISES",
        ">CNN BELIEVES",
        ">MSNBC HAS FOUND",
        ">PFIZER PROMISES",
        ">MODERNA GUARANTEES",
        ">STUDIES SHOW",
        ">EXPERTS SAY",
        ">TWATTER (((BLUECHECKMARK))) SAID",
        ">UNCONFIRMED BUT REALISTIC REPORTS",
        ">BASED ON RELIABLE SIMULATIONS",
        ">A SOURCE FROM UKRAINE",
        ">NATO ESTIMATES",
        ">JOE BIDEN SAID",
        ">AZOV COMMANDER SAID",
        ">INTERCEPTED COMMUNICATION",
        ">INTERCEPTED PHONE CALLS",
        ">RESPECTABLE SOURCE CLAIM",
    ] + [
        "это пойдёт в паблик 'жизнь насекомых'",
        "это хотя бы тысячник?",
        "очередной вскукарек...",
        "зарепортил",
        ">PESKOV SAID",
    ]

    if check_chance(0.7):
        stuff_twitter_retard_says = "\n".join(
            (
                ">ORYX SAYS",
                ">CONFIRMED BY VISUAL EVIDENCE",
                ">AUDIO REPORTS DETAIL",
                ">UKRANIAN MEDIA REPORTS",
                ">PENTAGON PROJECTS",
                ">U.K. SPY CHIEF INFORMS",
                ">UNCONFIRMED BUT REALISTIC REPORTS",
                ">ACCORDING TO ANALYSTS",
                ">THE UKRANIAN SECURITY SERVICE HAS ANNOUNCED",
                ">UKRANIAN INTELLIGENCE CLAIM",
                ">BELLINCUNT CONFIRMS",
                ">RUSSIAN (((DISSIDENT))) PREDICTS",
                ">PUBLIC SENTIMENT SUGGESTS",
                ">MULTIPLE REPORTS FROM BOTH SIDES",
                ">UNNAMED SOURCES CITED",
                ">ACCORDING TO UNNAMED (((WESTERN))) OFFICIALS",
                ">CITING UNNAMED WESTERN OFFICIALS",
                ">A SOURCE FAMILIAR WITH RUSSIAN THINKING",
                ">A SOURCE WHO SPOKE ON CONDITION OF ANONYMITY",
                ">US INTELLIGENCE REVEALS",
                ">UK INTELLIGENCE CONFIRMS",
                ">NEXTA SAYS",
                ">REUTERS SAYS",
                ">/K/ TOLD ME",
                ">US OFFICIALS SAY",
                ">PENTAGON SAYS",
                ">DOD BELIEVES",
                ">GENERAL MILLEY CONFIRMS",
                ">FBI AGREES",
                ">DIPLOMATS SURMISE",
                ">EU PROMISES",
                ">CNN BELIEVES",
                ">MSNBC HAS FOUND",
                ">PFIZER PROMISES",
                ">MODERNA GUARANTEES",
                ">STUDIES SHOW",
                ">EXPERTS SAY",
                ">TWATTER (((BLUECHECKMARK))) SAID",
                ">UNCONFIRMED BUT REALISTIC REPORTS",
                ">BASED ON RELIABLE SIMULATIONS",
                ">A SOURCE FROM UKRAINE",
                ">NATO ESTIMATES",
                ">JOE BIDEN SAID",
                ">AZOV COMMANDER SAID",
                ">PESKOV SAID",
                ">INTERCEPTED COMMUNICATION",
                ">INTERCEPTED PHONE CALLS",
            )
        )

    if not check_chance():
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=_to_code_block(random.choice(stuff_twitter_retard_says))
        if isinstance(stuff_twitter_retard_says, list)
        else _to_code_block(stuff_twitter_retard_says),
    )


@logged_context
def trista_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance(0.3):
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

    if not check_chance():
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

    if not check_chance(0.4):
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
def gym_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    if not check_chance():
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


@logged_context
def iscringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    if not is_reply(update):
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
        data: typing.Type[StaticReader] = None,
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
        data: typing.Type[StaticReader] = None,
    ) -> telegram.Message:
        return context.bot.send_photo(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            photo=cache.sniff_dog or data.sniff_dog,
        )

    choice_map = {"based": _process_based, "cringe": _process_cringe}

    return choice_map[random.choice(["based", "cringe"])](update, context, cache=cache, data=data)


@logged_context
def voice_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    voice_messages = [
        "как болезнь называется?",
        "пацаны, тут человеку руки оторвало!",
        "слова красивые, но ты пидор",
        "ничего не понял",
        "не могу послушать твоё голосове, мне оторвало уши",
        "пиши давай",
    ]

    if not check_chance():
        msg = voice_messages[random.randint(0, len(voice_messages) - 1)]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=msg,
        )

    return context.bot.sendSticker(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        sticker="CAACAgIAAxkBAAIBy2DHu6uTHF_uKSwtLRuWcUmHNHejAAI-AQAC39LPAoZ3xK3gRdEhHwQ",
    )
