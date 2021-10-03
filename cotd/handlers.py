import telegram
import telegram.ext


class FeatureHandler:
    # Value object for holding handler implementation function and expected handling method
    # So data and  code will be near one another
    # Example usage: FeatureHandler(implementation_function=question_mark, handler=telegram.ext.CommandHandler(["some","data"]))
    def __init__(self):
        raise NotImplementedError


def version_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    updater: telegram.ext.Updater
    return context.bot.send_message(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        text="666",
    )
