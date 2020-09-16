import random
import telegram
import telegram.ext
import logging


def unknown(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text="nope")


def start(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def cringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    try:
        return context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            sticker='CAACAgIAAxUAAV9fnDk1559P8eTSTmr6zhG-51cAA0AAAyYxpQgyTMNtqCOcyxsE')
    except AttributeError:
        return context.bot.send_sticker(
            chat_id=update.effective_chat.id,
            sticker='CAACAgIAAxUAAV9fnDk1559P8eTSTmr6zhG-51cAA0AAAyYxpQgyTMNtqCOcyxsE')


def iscringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
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
                text=open("static/cringe-sniff-dog.jpg", 'rb'))
    except AttributeError:
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Can"t see cringe though, reply to a cringe post')


def oldfellow(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/oldfellow.mp4', 'rb'))
    except AttributeError:
        return context.bot.send_video(
            chat_id=update.effective_chat.id, video=open('static/oldfellow.mp4', 'rb'))


def kekw(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    try:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=open('static/KEKW.mp4', 'rb'))
    except AttributeError:
        return context.bot.send_video(
            chat_id=update.effective_chat.id, video=open('static/KEKW.mp4', 'rb'))


def secret(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text='bit.ly/2Ro39uJ')
