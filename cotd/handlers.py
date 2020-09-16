from dataclasses import dataclass
import random
import telegram
import telegram.ext


class MediaCache:
    pass


CACHE = MediaCache()


def is_reply(update):
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
    return context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def iscringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:

    def _process_based(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:

        try:
            _ribnikov_file = CACHE.ribnikov
        except AttributeError:
            _ribnikov_file = open("static/ribnikov.based.mp4", 'rb')

        message = context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=_ribnikov_file)

        try:
            CACHE.ribnikov
        except AttributeError:
            CACHE.ribnikov = message.video.file_id

        return message

    def _process_cringe(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:

        try:
            _sniff_dog_file = CACHE.sniff
        except AttributeError:
            _sniff_dog_file = open("static/cringe-sniff-dog.jpg", 'rb')

        message = context.bot.send_photo(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            photo=_sniff_dog_file)

        try:
            CACHE.sniff
        except AttributeError:
            CACHE.sniff = message.photo[0].file_id

        return message

    choice_map = {'based': _process_based, 'cringe': _process_cringe}

    if not is_reply(update):
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Can"t see cringe though, reply to a cringe post')
        context.dispatcher.logger.debug(message)
        return message

    message = choice_map[random.choice(["based", "cringe"])](update, context)

    context.dispatcher.logger.debug(message)
    return message


def oldfellow(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    try:
        _oldfellow_file = CACHE.oldfellow
    except AttributeError:
        _oldfellow_file = open("static/oldfellow.mp4", 'rb')

    if not is_reply(update):
        message = context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=_oldfellow_file)
    else:
        message = context.bot.send_video(chat_id=update.effective_chat.id, video=_oldfellow_file)

    try:
        CACHE.oldfellow
    except AttributeError:
        CACHE.oldfellow = message.video.file_id

    context.dispatcher.logger.debug(message)
    return message


def kekw(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    try:
        _kekw_file = CACHE.kekw
    except AttributeError:
        _kekw_file = open('static/KEKW.mp4', 'rb')

    if not is_reply(update):
        message = context.bot.send_video(chat_id=update.effective_chat.id, video=_kekw_file)
    else:
        message = context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=_kekw_file)

    try:
        CACHE.kekw
    except AttributeError:
        CACHE.kekw = message.video.file_id

    context.dispatcher.logger.debug(message)
    return message


def secret(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text='bit.ly/2Ro39uJ')
