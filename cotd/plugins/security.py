import telegram
import telegram.error
import telegram.ext
from cotd.plugins.helpers import logged_context


@logged_context
def check_allowed_sources(update: telegram.Update, context: telegram.ext.CallbackContext):
    """security plugin to check if message is coming from trusted sources"""
    pass
    # # TODO: add check if user that writes inline message is in trusted group
    # try:
    #     if update.effective_chat:

    #         if x == update.effective_chat.chat.id:
    #             return True
    # except AssertionError:
    #     context.dispatcher.logger.debug(
    #         f"{update.message} was sent from untrusted source and stopped from handling"
    #     )
    #     raise telegram.ext.DispatcherHandlerStop
