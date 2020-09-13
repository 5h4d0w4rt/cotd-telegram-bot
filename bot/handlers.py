import random

# TODO create class
# that logs every handler call
# so we do not need to implement logging for every handler out there


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="nope")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def cringe(update, context):
    try:
        return context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            sticker=open('static/smileyOne.webp', 'rb'))
    except AttributeError:
        return context.bot.send_sticker(chat_id=update.effective_chat.id,
                                        sticker=open('static/smileyOne.webp',
                                                     'rb'))


def iscringe(update, context):
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
        return context.bot.send_message(chat_id=update.effective_chat.id,
                                        text='Can"t see cringe though')


def oldfellow(update, context):
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/oldfellow.mp4', 'rb'))
    except AttributeError:
        context.bot.send_video(chat_id=update.effective_chat.id,
                               video=open('static/oldfellow.mp4', 'rb'))


def kekw(update, context):
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/KEKW.mp4', 'rb'))
    except AttributeError:
        return context.bot.send_video(chat_id=update.effective_chat.id,
                                      video=open('static/KEKW.mp4', 'rb'))


def secret(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='bit.ly/2Ro39uJ')
