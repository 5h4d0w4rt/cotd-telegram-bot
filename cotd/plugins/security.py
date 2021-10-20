import telegram
import telegram.error
import telegram.ext
from cotd.plugins.helpers import logged_context


@logged_context
def check_allowed_sources(update: telegram.Update, context: telegram.ext.CallbackContext,
trusted_sources: dict):
    """security plugin to check if message is coming from trusted sources"""
    match type(update.effective_chat):
        case None:
            # nothing to check
            return None
        case telegram.Chat:
            assert update.effective_chat is not None
            if not (update.effective_chat.id in trusted_sources['chats']):
                context.dispatcher.logger.debug(
                    f"{update.message} was sent from untrusted source and stopped from handling"
            )
            raise telegram.ext.DispatcherHandlerStop
    # # TODO: add check if user that writes inline message is in trusted group
    # try:
    #     if update.effective_chat:

    #         if x == update.effective_chat.chat.id:
    #             return True
    # except AssertionError:
    #
