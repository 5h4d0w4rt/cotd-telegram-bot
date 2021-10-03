import telegram
import telegram.ext
import random
import typing
from PIL import Image, ImageFont, ImageDraw
import io
import uuid


def motivation_handler_v2(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:
    query = update.inline_query.query
    if query == "":
        return

    results = [
        telegram.InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="pososi)",
            input_message_content=telegram.InputTextMessageContent(query + " еблан"),
        ),
    ]
    update.inline_query.answer(results)

    # if random.randint(0, 4) == 1:
    #     return context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text="да забей, чел",
    #     )
    # image = Image.open("static/motivator.jpg")


#     fontsize = 1  # starting font size

#     # portion of image width you want text width to be
#     img_fraction = 0.50

#     font = ImageFont.truetype("static/lobster.ttf", fontsize)
#     while font.getsize(query)[0] < img_fraction * image.size[0]:
#         # iterate until the text size is just larger than the criteria
#         fontsize += 1
#         font = ImageFont.truetype("static/lobster.ttf", fontsize)

#     image_editable = ImageDraw.Draw(image)
#     W, H = image.size
#     w, h = image_editable.textsize(query, font)

#     width = (W - w) / 2
#     heigh = h / 5
#     # some color const
#     msg_color = "#FFFFFF"
#     shadow_color = "#121212"
#     # add shadow
#     image_editable.text((width - 2, heigh), query, font=font, fill=shadow_color)
#     image_editable.text((width + 2, heigh), query, font=font, fill=shadow_color)
#     image_editable.text((width, heigh - 2), query, font=font, fill=shadow_color)
#     image_editable.text((width, heigh + 2), query, font=font, fill=shadow_color)
#     # add text
#     image_editable.text((width, heigh), query, font=font, fill=msg_color)
#     # fake save
#     bio = io.BytesIO()
#     bio.name = "image.jpeg"
#     image.save(bio, "JPEG")
#     bio.seek(0)
