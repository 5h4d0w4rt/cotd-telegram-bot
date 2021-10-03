import telegram
import telegram.error
import telegram.ext
from cotd.plugins.helpers import logged_context


@logged_context
def check_allowed_sources(update: telegram.Update, context: telegram.ext.CallbackContext):
    """security plugin to check if message is coming from trusted sources"""
    # TODO: add check if user that writes inline message is in trusted group
    try:
        if update.effective_chat:
            assert update.effective_message.chat.id in (
                context.dispatcher._cotd_db,
                context.dispatcher._cotd_group,
            )
    except AssertionError:
        context.dispatcher.logger.debug(
            "Message was sent from untrusted source and stopped from handling"
        )
        raise telegram.ext.DispatcherHandlerStop
