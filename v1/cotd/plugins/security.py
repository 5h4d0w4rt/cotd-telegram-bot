import telegram
import telegram.error
import telegram.ext

from v1.cotd.plugins.helpers import logged_context


@logged_context
def check_allowed_sources(
    update: telegram.Update, context: telegram.ext.CallbackContext, trusted_sources: dict
):
    """security plugin to check if message is coming from trusted sources"""
    match type(update.effective_chat):
        case telegram.Chat:
            assert update.effective_chat is not None
            if not (int(update.effective_chat.id) in trusted_sources["chats"]):
                context.dispatcher.logger.info(
                    f"{update.message} was sent from untrusted source and stopped from handling"
                )
            raise telegram.ext.DispatcherHandlerStop
        case _:
            return None
    # # TODO: add check if user that writes inline message is in trusted group
