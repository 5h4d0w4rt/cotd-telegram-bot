import time
import uuid

import cotd
import ratelimit
import telegram
import telegram.ext
from cotd.plugins.misc import oldfellow_inline_impl
from cotd.plugins.motivationv2 import motivation_inline_impl

ONE_SECOND = 1

@ratelimit.sleep_and_retry
@ratelimit.limits(
    calls=1, period=ONE_SECOND
)  # recommended per https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
def menu(update: telegram.Update, context: telegram.ext.CallbackContext) -> bool:
    if update.inline_query.query:
        match update.inline_query.query:
            case "menu" | "меню":
                return update.inline_query.answer([oldfellow_inline_impl(update, context)])
            case _:
                return update.inline_query.answer([motivation_inline_impl(update, context)])
    return update.inline_query.answer([])
