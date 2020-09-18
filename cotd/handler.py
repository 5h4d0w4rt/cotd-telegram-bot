import telegram
import telegram.ext
from dataclasses import dataclass
import random
import abc
import typing
import cotd.static


class MediaCache(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def __getattribute__(self, name: str) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setattr__(self, name: str, value: typing.Any) -> None:
        raise NotImplementedError


class MediaCacheInMemory(MediaCache):

    def __init__(self):
        pass

    def __getattribute__(self, name: str) -> typing.Union[typing.Any, None]:
        try:
            result = object.__getattribute__(self, name)
        except AttributeError:
            return None
        else:
            return result

    def __setattr__(self, name: str, value: typing.Any) -> None:
        object.__setattr__(self, name, value)


@dataclass
class HandlerHolderConfig:
    cache: typing.Type[MediaCache]
    data: typing.Type[cotd.static.Static]


class HandlerHolder:

    def __init__(self, config: HandlerHolderConfig):
        self.cache = config.cache
        self.data = config.data

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
            update: telegram.Update,
            context: telegram.ext.CallbackContext,
        ) -> telegram.Message:

            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=self.cache.ribnikov or self.data.ribnikov)

            if not self.cache.ribnikov:
                self.cache.ribnikov = message.video.file_id

            return message

        def _process_cringe(
            update: telegram.Update,
            context: telegram.ext.CallbackContext,
        ) -> telegram.Message:

            message = context.bot.send_photo(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                photo=self.cache.sniff_dog or self.data.sniff_dog)

            if not self.cache.sniff_dog:
                self.cache.sniff_dog = message.photo[0].file_id

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

        if not self._is_reply(update):
            message = context.bot.send_video(
                chat_id=update.effective_chat.id, video=self.cache.oldfellow or self.data.oldfellow)
        else:
            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=self.cache.oldfellow or self.data.oldfellow)

        if not self.cache.oldfellow:
            self.cache.oldfellow = message.video.file_id

        context.dispatcher.logger.debug(message)
        return message

    def kekw(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:

        if not self._is_reply(update):
            message = context.bot.send_video(
                chat_id=update.effective_chat.id, video=self.cache.kekw or self.data.kekw)
        else:
            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=self.cache.kekw or self.data.kekw)

        if not self.cache.kekw:
            self.cache.kekw = message.video.file_id

        context.dispatcher.logger.debug(message)
        return message

    def goaway(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:

        if not self._is_reply(update):
            message = context.bot.send_video(
                chat_id=update.effective_chat.id, video=self.cache.go_away or self.data.go_away)
        else:
            message = context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.reply_to_message.message_id,
                video=self.cache.go_away or self.data.go_away)

        if not self.cache.go_away:
            self.cache.go_away = message.video.file_id

        context.dispatcher.logger.debug(message)
        return message

    def secret(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> telegram.Message:
        return context.bot.send_message(chat_id=update.effective_chat.id, text='bit.ly/2Ro39uJ')

    def cotd(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> None:
        print(context.bot.get_chat(chat_id=update.effective_chat.id))

    def cache_users(
        self,
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ) -> None:
        pass
        # setattr(self.cache, str(update.effective_chat.title), str(update.effective_chat.id))
        # setattr(self.cache, str(update.effective_user.username), str(update.effective_user.id))
        # getattr(self.cache, str(update.effective_chat.title))
        # getattr(self.cache, str(update.effective_chat.username))