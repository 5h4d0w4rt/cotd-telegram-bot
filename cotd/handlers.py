import random
import telegram
import telegram.ext
# TODO create class
# that logs every handler call
# so we do not need to implement logging for every handler out there


def unknown(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="nope")


def start(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def cringe(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    try:
        return context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            sticker=open('static/smileyOne.webp', 'rb'))
    except AttributeError:
        return context.bot.send_sticker(
            chat_id=update.effective_chat.id, sticker=open('static/smileyOne.webp', 'rb'))


def iscringe(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    choices = ["based", "cringe"]
    final_choice = random.choice(choices)
    try:
        if final_choice == 'based':
            return context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=open("static/ribnikov.based.mp4", 'rb'))
        if final_choice == 'cringe':
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                text="yep, it's cringe")
    except AttributeError:
        return context.bot.send_message(
            chat_id=update.effective_chat.id, text='Can"t see cringe though')


def oldfellow(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/oldfellow.mp4', 'rb'))
    except AttributeError:
        context.bot.send_video(
            chat_id=update.effective_chat.id, video=open('static/oldfellow.mp4', 'rb'))


def kekw(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/KEKW.mp4', 'rb'))
    except AttributeError:
        return context.bot.send_video(
            chat_id=update.effective_chat.id, video=open('static/KEKW.mp4', 'rb'))


def secret(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='bit.ly/2Ro39uJ')
