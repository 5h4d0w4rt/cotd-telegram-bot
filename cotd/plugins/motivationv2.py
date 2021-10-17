import io
import typing
import uuid

import ratelimit
import telegram
import telegram.ext
from cotd.plugins.helpers import make_image
from PIL import Image

ONE_SECOND = 1


def motivation_inline(
    update: telegram.Update, context: telegram.ext.CallbackContext
) -> telegram.InlineQueryResultCachedPhoto:
    db = context.dispatcher._cotd_db
    query = update.inline_query.query
    if query == "":
        return

    motivation_image = make_image(Image.open("static/motivator.jpg"), query, "top")

    msg = context.bot.send_photo(
        chat_id=db,
        photo=motivation_image,
    )
    photo_id = msg.photo[0].file_id
    context.bot.delete_message(chat_id=db, message_id=msg.message_id)
    return telegram.InlineQueryResultCachedPhoto(
        id=str(uuid.uuid4()),
        title="CachedPhoto",
        photo_file_id=photo_id,
    )
