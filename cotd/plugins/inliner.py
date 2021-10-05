import functools
import random
import typing
import uuid
import telegram
import ratelimit
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, is_reply, logged_context
from cotd.plugins.motivationv2 import ONE_SECOND, _motivation_impl
from cotd.plugins.misc import _oldfellowinline_impl
from cotd.static import StaticReader

ONE_SECOND = 1


@ratelimit.sleep_and_retry
@ratelimit.limits(
    calls=1, period=ONE_SECOND
)  # recommended per https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
def menu(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.inline_query.answer(
        [_motivation_impl(update, context), _oldfellowinline_impl(update, context)]
    )
