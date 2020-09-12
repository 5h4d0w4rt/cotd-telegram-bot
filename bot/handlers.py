def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")


def cringe(update, context):
    context.bot.send_sticker(chat_id=update.effective_chat.id,
                             sticker=open('static/smileyOne.webp', 'rb'))


def oldfellow(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id,
                           video=open('static/oldfellow.mp4', 'rb'))
