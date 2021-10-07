import functools
import random
import telegram
import telegram.ext
import typing
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, logged_context
from cotd.static import StaticReader


@logged_context
@functools.partial(cacheable_handler, key="sf", path="photo[0].file_id")
def cuno_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
    cache: typing.Type[MediaCache] = None,
    data: typing.Type[StaticReader] = None,
) -> typing.Union[telegram.Message, None]:
    if random.randint(0, 1) != 0:
        return None

    return context.bot.send_photo(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        photo=cache.sf or data.sf,
    )
