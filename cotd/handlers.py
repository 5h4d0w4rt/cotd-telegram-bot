import telegram
import telegram.ext
import random
import typing
import datetime
import functools

from cotd.cacher import MediaCache
from cotd.static import Static

from PIL import Image, ImageFont, ImageDraw

from io import BytesIO


class FeatureHandler:
    # Value object for holding handler implementation function and expected handling method
    # So data and  code will be near one another
    # Example usage: FeatureHandler(implementation_function=question_mark, handler=telegram.ext.CommandHandler(["some","data"]))
    def __init__(self):
        raise NotImplementedError


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

    reaction_text = 'пизда'

    if random.randint(0, 5) == 3:
        reaction_text = '1/5, чел'

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=reaction_text,
    )


@logged_context
def stalker_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 5) != 3:
        return None

    roll_map = {
        10: "Ну ты выдал!",
        20: "Блин, так не смешно же.",
        30: "А поновее ничего нет?",
        40: "Ору!",
        50: "я плакал",
        60: "ха-ха-ха",
        70: "*выдыхает через нос*",
        80: "рофл",
        90: "ржака",
        100: "спизданул как боженька",
    }

    decision = roll_map.get(random.randint(0, 100))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=decision,
    )


manet_messages = [
    "ля как красиво",
    "нет сил наэто смотретб слишком кросива",
    "к паническим атакам готов",
    "банжур ебать",
    "ты шо ебанутый шо ты там делаешь?",
    "ебучая сингулярность",
    "это могли быть мы",
    "F L E X",
    "АААААААаааААААААа",
    "время дрочитб",
    "*немой крик*",
    "Любовь в каждом пикселе",
    "Фото, заряженное на позитив",
    "Как мало нужно для счастья",
    "Досадно, но ладно",
    "Эта лайф в кайф",
    "Good vibes only",
    "big mood",
    "Chilling",
    "Bon Appetit",
    "Фотоотчет для мамы",
    "Фото без подписи",
    "Неуникальный контент",
    "Наконец-то, пятница",
    "Райское место",
    "Остановись, мгновенье!",
    "Я смог, значит, и вы сможете",
    "Все в ваших руках!",
    "Сегодня, тот самый день.",
    "Рабочего характера",
    "Поставлю класс, но это из вежливости",
    "Заберите меня отсюда(((",
    "18+",
    "Натуралов на помойку",
    "держись, брат",
    "Работать трудно",
    "Военные преступления",
    "Haters gonna hate",
    "так и живем",
    "автор - мудак",
    "кладмен - мудак",
    "узнали? согласны?",
    "nice",
    "CUM",
]


@logged_context
def manet_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 4) != 2:
        return None

    i = random.randint(0, len(manet_messages)-1)
    msg = manet_messages[i]

    file_info = context.bot.get_file(update.message.photo[-1].file_id)
    file = file_info.download()
    image = Image.open(file)

    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.50

    font = ImageFont.truetype('static/lobster.ttf', fontsize)
    while font.getsize(msg)[0] < img_fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype('static/lobster.ttf', fontsize)

    image_editable = ImageDraw.Draw(image)
    W, H = image.size
    w, h = image_editable.textsize(msg, font)

    width = (W-w)/2
    heigh = (H-h)/1.1
    # some color const
    msg_color = "#FFFFFF"
    shadow_color = "#121212"
    # add shadow
    image_editable.text((width-2, heigh), msg, font=font, fill=shadow_color)
    image_editable.text((width+2, heigh), msg, font=font, fill=shadow_color)
    image_editable.text((width, heigh-2), msg, font=font, fill=shadow_color)
    image_editable.text((width, heigh+2), msg, font=font, fill=shadow_color)
    # add text
    image_editable.text((width,heigh), msg, font=font, fill=msg_color)
    # fake save
    bio = BytesIO()
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=bio,
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

    decision = roll_map.get(random.randint(0, 10))
    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )



@logged_context
@functools.partial(cacheable_handler, key="stuffy", path="photo[0].file_id")
def stuffy_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 5) != 3:
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.stuffy or data.stuffy,
    )

@logged_context
@functools.partial(cacheable_handler, key="journalism", path="photo[0].file_id")
def journalism_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[Static] = None,
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
        9: "а что сказать то хотел?",
        12: "интересное чтиво",
    }
    decision = roll_map.get(random.randint(0, 12))

    if not decision:
        return None

    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text=decision,
    )

voice_messages = [
    "как болезнь называется?",
    "пацаны, тут человеку руки оторвало!",
    "слова красивые, но ты пидор",
    "ничего не понял",
    "не могу послушать твоё голосове, мне оторвало уши",
    "пиши давай",
]

@logged_context
def voice_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 5) != 3:
        msg = manet_messages[random.randint(0, len(voice_messages)-1)]

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
