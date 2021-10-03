import telegram
import telegram.ext
import telegram.error
from cotd.handlers import logged_context


class SourceNotAllowedError(telegram.error.TelegramError):
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__("Message was sent from untrusted source")


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
        raise telegram.ext.DispatcherHandlerStop
