import datetime
import random
import typing

import telegram
import telegram.ext
from cotd.plugins.helpers import logged_context, make_image, check_timer, day_of_week
from PIL import Image


# kandinsky_handler - list of reactions.
kandinsky_messages = [
    "Наконец-то!",
    "выбери жизнь",
    "yea...",
    "с подвохом",
    "норм за свои деньги",
    "по акции взял",
    "перемога",
    "зрада",
    "ауф",
    "счастья, здоровья",
    "Bruh",
    "при сталине такого не было",
    "инвестировал в говно",
    "четыре",
    "за мат извени",
    "What Zero Pussy Does to a MF",
    "сколько жмешь?",
    "у кого то будет секс...",
    "найди работу еблан",
    "прости если трахнул",
    "ля как красиво",
    "нет сил наэто смотретб слишком кросива",
    "к паническим атакам готов",
    "банжур ебать",
    "ты шо ебанутый шо ты там делаешь?",
    "ебучая сингулярность",
    "это могли быть мы",
    "АААААААаааААААААа",
    "время дрочитб",
    "*немой крик*",
    "Любовь в каждом пикселе",
    "Как мало нужно для счастья",
    "Досадно, но ладно",
    "Эта лайф в кайф",
    "Good vibes only",
    "Chilling",
    "Bon Appetit",
    "Фотоотчет для мамы",
    "Фото без подписи",
    "Неуникальный контент",
    "Остановись, мгновенье!",
    "Я смог, значит, и вы сможете",
    "Все в ваших руках!",
    "Сегодня, тот самый день.",
    "Рабочего характера",
    "18+",
    "Натуралов на помойку",
    "держись, брат",
    "Работать трудно",
    "Военные преступления",
    "Haters gonna hate",
    "так и живем",
    "автор - мудак",
    "узнали? согласны?",
    "nice",
    "refuse to elaborate further",
    "сестра где твой хиджаб?",
    "кринж",
    "big mood",
    "CUM",
    "F L E X",
    "Фото, заряженное на позитив",
    "прошлогодний мэм",
    "мы",
    "если бы мы знали что это такое",
]

kandinsky_max = 1  # TODO: rename
kandinsky_chances = {}  # TODO: rename
kandinsky_last = datetime.datetime.now()


@logged_context
def kandinsky_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    if not _chance(0.4): 
        return None

    global kandinsky_last

    now = datetime.datetime.now()
    time_diff = now - kandinsky_last

    if time_diff.total_seconds() < 240:
        return None

    kandinsky_last = now

    x = 0
    i = 0
    msg = ""

    # make histogram https://numpy.org/doc/stable/reference/generated/numpy.histogram.html
    # store on bot
    # use value from distribution
    global kandinsky_max

    # correct the frequency of using phrases
    while x == 0:
        i = random.randint(0, len(kandinsky_messages) - 1)

        chance = kandinsky_chances.get(i, -1)

        if chance == kandinsky_max:
            kandinsky_max = kandinsky_max + 1
            continue

        if chance > kandinsky_max:
            kandinsky_max = chance
            continue

        if chance < kandinsky_max:
            kandinsky_chances[i] = chance + 1

            msg = kandinsky_messages[i]

            # ахаха, что ты мне сделаешь, я в другом городе
            if i == 0:
                msg = "Наконец-то, " + day_of_week() + "!"

            break

    file_info = context.bot.get_file(update.message.photo[-1].file_id)

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=make_image(Image.open(file_info.download()), msg, "bottom"),  # TODO: move to const.
    )
