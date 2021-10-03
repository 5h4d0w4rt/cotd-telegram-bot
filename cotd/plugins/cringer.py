import functools
import random
import typing

import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, logged_context, is_reply
from cotd.static import StaticReader


@logged_context
def iscringe(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> telegram.Message:
    if not is_reply(update):
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Can"t see cringe though, reply to a cringe post',
        )

    @functools.partial(cacheable_handler, key="ribnikov", path="video.file_id")
    @logged_context
    def _process_based(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
        cache: typing.Type[MediaCache] = None,
        data: typing.Type[StaticReader] = None,
    ) -> telegram.Message:
        return context.bot.send_video(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            video=cache.ribnikov or data.ribnikov,
        )

    @functools.partial(cacheable_handler, key="sniff_dog", path="photo[0].file_id")
    @logged_context
    def _process_cringe(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
        cache: typing.Type[MediaCache] = None,
        data: typing.Type[StaticReader] = None,
    ) -> telegram.Message:
        return context.bot.send_photo(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.reply_to_message.message_id,
            photo=cache.sniff_dog or data.sniff_dog,
        )

    choice_map = {"based": _process_based, "cringe": _process_cringe}

    return choice_map[random.choice(["based", "cringe"])](update, context, cache=cache, data=data)
