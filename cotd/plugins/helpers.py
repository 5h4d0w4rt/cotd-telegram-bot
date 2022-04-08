import functools
from importlib.resources import path
import logging
import telegram
import telegram.ext
import logging
import typing
import io
import pathlib
import random
import datetime
import subprocess

from PIL import Image, ImageDraw, ImageFont


def logged_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        old_factory = logging.getLogRecordFactory()

        def _record_factory(*args, **kwargs):
            """Make function print wrapped function's name instead of a wrapper"""
            record = old_factory(*args, **kwargs)
            record.funcName = f.__name__
            return record

        dispatcher: telegram.ext.Dispatcher = args[1].dispatcher

        logging.setLogRecordFactory(_record_factory)
        dispatcher.logger.info(args)
        dispatcher.logger.info(kwargs)
        dispatcher.logger.debug(dispatcher.bot_data)
        dispatcher.logger.debug(dispatcher.chat_data)
        dispatcher.logger.debug(dispatcher.user_data)
        result = f(*args, **kwargs)
        dispatcher.logger.info(f"{f.__name__} : {result}")
        logging.setLogRecordFactory(old_factory)

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


# TODO: fontsize for small text
def make_image(image, text: str, pos: str) -> io.BytesIO:
    width, heigh = 0, 0  # init
    fontsize = 10  # starting font size
    img_fraction = 0.50  # portion of image width you want text width to be

    font = ImageFont.truetype("static/lobster.ttf", fontsize, encoding="unic")
    while font.getsize(text)[0] < img_fraction * image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("static/lobster.ttf", fontsize, encoding="unic")

    image_editable = ImageDraw.Draw(image)

    W, H = image.size
    w, h = image_editable.textsize(text, font)

    if pos == "bottom":
        width = (W - w) / 2
        heigh = (H - h) / 1.01
    else:
        width = (W - w) / 2
        heigh = h / 5

    # some color const
    # TODO: move out to const
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


def check_chance(percent: float = 0.5):
    return round(random.random(), 1) < percent


def check_timer(now: datetime.datetime, timer: datetime.datetime, threshold: int):
    return (now - timer).total_seconds() < threshold
