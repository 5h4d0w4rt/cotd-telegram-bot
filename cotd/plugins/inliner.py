import time
import typing
import uuid

import cotd
import ratelimit
import telegram
import telegram.ext
from cotd.plugins.misc import oldfellow_inline
from cotd.plugins.motivationv2 import motivation_inline
from cotd.plugins.webm_to_mp4 import webm_to_mp4_inline
from cotd.static import StaticReader
import re

ONE_SECOND = 1


@ratelimit.sleep_and_retry
@ratelimit.limits(
    calls=1, period=ONE_SECOND
)  # recommended per https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
def menu(
    update: telegram.Update, context: telegram.ext.CallbackContext, data: typing.Type[StaticReader]
) -> bool:
    if update.inline_query.query:
        # generic matcher
        match update.inline_query.query:
            case "menu" | "меню":
                return update.inline_query.answer([oldfellow_inline(update, context, data)])
            case _:
                return update.inline_query.answer([motivation_inline(update, context)])

    return update.inline_query.answer([])
