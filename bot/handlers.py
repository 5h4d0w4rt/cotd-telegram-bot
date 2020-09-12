def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="nope")

def start(update, context):
    pass
    # if update.effective_message.reply_to_message:
    #     context.bot.send_message(
    #         chat_id=update.effective_message.reply_to_message['message_id'],
    #         text=f"{update.effective_message}")
    # else:
    context.bot.send_message(chat_id=update.effective_chat.id, text="start")

def cringe(update, context):
    if hasattr(update.message.reply_to_message,'message_id'):
        context.bot.send_sticker(chat_id=update.effective_chat.id,          
                                reply_to_message_id=update.message.reply_to_message.message_id,
                                sticker=open('static/smileyOne.webp', 'rb'))
    else:
        context.bot.send_sticker(chat_id=update.effective_chat.id,          
                                sticker=open('static/smileyOne.webp', 'rb'))

def oldfellow(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id,
                           video=open('static/oldfellow.mp4', 'rb'))

def kekw(update, context):
    context.bot.send_video(chat_id=update.effective_chat.id,
                           video=open('static/KEKW.mp4', 'rb'))
