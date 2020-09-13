import random


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="nope")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def cringe(update, context):
    if hasattr(update.message.reply_to_message, 'message_id'):
        context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            sticker=open('static/smileyOne.webp', 'rb'))
    else:
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker=open('static/smileyOne.webp', 'rb'))


def iscringe(update, context):
    if hasattr(update.message.reply_to_message, 'message_id'):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            text=random.choice(["это база", "это кринж"]))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Где кринж?')


def oldfellow(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id,
                           video=open('static/oldfellow.mp4', 'rb'))


def kekw(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id,
                           video=open('static/KEKW.mp4', 'rb'))


def secret(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='bit.ly/2Ro39uJ')
