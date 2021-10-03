import telegram
import telegram.ext
import ratelimit
import typing
from PIL import Image, ImageFont, ImageDraw
import io
import uuid
from cotd.plugins.helpers import logged_context, make_image

ONE_SECOND = 1


@ratelimit.sleep_and_retry
@ratelimit.limits(
    calls=1, period=ONE_SECOND
)  # recommended per https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
def motivation_handler_v2(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    db = context.dispatcher._cotd_db
    results = []
    query = update.inline_query.query
    if query == "":
        return

    motivation_image = make_image(Image.open("static/motivator.jpg"), query)

    msg = context.bot.send_photo(
        chat_id=db,
        photo=motivation_image,
    )
    photo_id = msg.photo[0].file_id
    context.bot.delete_message(chat_id=db, message_id=msg.message_id)

    results.append(
        telegram.InlineQueryResultCachedPhoto(
            id=str(uuid.uuid4()),
            title="CachedPhoto",
            photo_file_id=photo_id,
        )
    )

    update.inline_query.answer(results)
