import telegram
import telegram.ext
from dataclasses import dataclass
import random
import abc
import typing


class MediaCache(abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def __getattribute__(self, name: str) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setattr__(self, name: str, value: typing.Any) -> None:
        raise NotImplementedError


class MediaCacheInMemory:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def __getattribute__(self, name: str) -> typing.Any:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        super().__setattr__(name, value)


@dataclass
class HandlerHolderConfig:
    cache: MediaCache


class HandlerHolder:

    def __init__(self, config: HandlerHolderConfig):
        self.cache = config.cache

    def _is_reply(self, update):
        try:
            update.message.reply_to_message.message_id
        except AttributeError:
            return False
        else:
            return True

    def start(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:
        return context.bot.send_message(chat_id=update.effective_chat.id, text="start")

    def iscringe(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:

        def _process_based(
            self,
            update: telegram.Update,
            context: telegram.ext.CallbackContext,
        ) -> telegram.Message:

            try:
                _ribnikov_file = self.cache.ribnikov
            except AttributeError:
                _ribnikov_file = open("static/ribnikov.based.mp4", 'rb')

            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=_ribnikov_file)

            try:
                self.cache.ribnikov
            except AttributeError:
                self.cache.ribnikov = message.video.file_id

            return message

        def _process_cringe(
            self,
            update: telegram.Update,
            context: telegram.ext.CallbackContext,
        ) -> telegram.Message:

            try:
                _sniff_dog_file = self.cache.sniff
            except AttributeError:
                _sniff_dog_file = open("static/cringe-sniff-dog.jpg", 'rb')

            message = context.bot.send_photo(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                photo=_sniff_dog_file)

            try:
                self.cache.sniff
            except AttributeError:
                self.cache.sniff = message.photo[0].file_id

            return message

        choice_map = {'based': _process_based, 'cringe': _process_cringe}

        if not self._is_reply(update):
            message = context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Can"t see cringe though, reply to a cringe post')
            context.dispatcher.logger.debug(message)
            return message

        message = choice_map[random.choice(["based", "cringe"])](update, context)

        context.dispatcher.logger.debug(message)
        return message

    def oldfellow(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:
        try:
            _oldfellow_file = self.cache.oldfellow
        except AttributeError:
            _oldfellow_file = open("static/oldfellow.mp4", 'rb')

        if not self._is_reply(update):
            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=_oldfellow_file)
        else:
            message = context.bot.send_video(
                chat_id=update.effective_chat.id, video=_oldfellow_file)

        try:
            self.cache.oldfellow
        except AttributeError:
            self.cache.oldfellow = message.video.file_id

        context.dispatcher.logger.debug(message)
        return message

    def kekw(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:
        try:
            _kekw_file = self.cache.kekw
        except AttributeError:
            _kekw_file = open('static/KEKW.mp4', 'rb')

        if not self._is_reply(update):
            message = context.bot.send_video(chat_id=update.effective_chat.id, video=_kekw_file)
        else:
            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=_kekw_file)

        try:
            self.cache.kekw
        except AttributeError:
            self.cache.kekw = message.video.file_id

        context.dispatcher.logger.debug(message)
        return message

    def secret(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:
        return context.bot.send_message(chat_id=update.effective_chat.id, text='bit.ly/2Ro39uJ')
