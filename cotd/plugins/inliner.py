import functools
import random
import typing
import uuid
import telegram
import telegram.ext
from cotd.cacher import MediaCache
from cotd.plugins.helpers import cacheable_handler, is_reply, logged_context
from cotd.plugins.motivationv2 import _motivation_impl
from cotd.plugins.misc import _oldfellowinline_impl
from cotd.static import StaticReader


def menu(update: telegram.Update, context: telegram.ext.CallbackContext):
    results = [_oldfellowinline_impl(update, context), _motivation_impl(update, context)]
    update.inline_query.answer(results)
