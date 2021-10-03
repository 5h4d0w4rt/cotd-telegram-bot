import functools
import telegram
import telegram.ext

import typing
import io
from PIL import Image, ImageDraw, ImageFont


def logged_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        dispatcher: telegram.ext.Dispatcher = args[1].dispatcher

        dispatcher.logger.debug(args)
        dispatcher.logger.debug(kwargs)

        dispatcher.logger.debug(dispatcher.bot_data)
        dispatcher.logger.debug(dispatcher.chat_data)
        dispatcher.logger.debug(dispatcher.user_data)

        result = f(*args, **kwargs)
        dispatcher.logger.debug(f"{f.__name__} : {result}")

        return result

    return wrapper


def cacheable_handler(f, key: typing.Any, path: str):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):

        if "cache" not in kwargs:
            return f(*args, **kwargs)

        cache = kwargs["cache"]
        result = f(*args, **kwargs)
        if not cache.key:
            setattr(cache, key, functools.reduce(getattr, path.split("."), result))

        return result

    return wrapper


def is_reply(update: telegram.Update):
    try:
        update.message.reply_to_message.message_id
    except AttributeError:
        return False
    else:
        return True


def make_image(image, text: str) -> io.BytesIO:
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
