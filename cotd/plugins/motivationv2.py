import telegram
import telegram.ext
import ratelimit
import typing
from PIL import Image, ImageFont, ImageDraw
import io
import uuid
from cotd.handlers import logged_context

ONE_SECOND = 1


def make_picture(text):
    image = Image.open("static/motivator.jpg")

    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.50

    font = ImageFont.truetype("static/lobster.ttf", fontsize)
    while font.getsize(text)[0] < img_fraction * image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("static/lobster.ttf", fontsize)
    image_editable = ImageDraw.Draw(image)
    W, H = image.size
    w, h = image_editable.textsize(text, font)

    width = (W - w) / 2
    heigh = h / 5
    # some color const
    msg_color = "#FFFFFF"
    shadow_color = "#121212"
    # add shadow
    image_editable.text((width - 2, heigh), text, font=font, fill=shadow_color)
    image_editable.text((width + 2, heigh), text, font=font, fill=shadow_color)
    image_editable.text((width, heigh - 2), text, font=font, fill=shadow_color)
    image_editable.text((width, heigh + 2), text, font=font, fill=shadow_color)
    # add text
    image_editable.text((width, heigh), text, font=font, fill=msg_color)
    # fake save
    bio = io.BytesIO()
    bio.name = "image.jpeg"
    image.save(bio, "JPEG")
    bio.seek(0)

    return bio


@ratelimit.sleep_and_retry
@ratelimit.limits(
    calls=1, period=ONE_SECOND
)  # recommended per https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
def motivation_handler_v2(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    db = -1001530261511
    results = []
    query = update.inline_query.query
    if query == "":
        return

    motivation_picture = make_picture(query)

    msg = context.bot.send_photo(
        chat_id=db,
        photo=motivation_picture,
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
