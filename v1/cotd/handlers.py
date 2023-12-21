import functools
import typing

import telegram
import telegram.ext

import v1.cotd.cacher
import v1.cotd.service
import v1.cotd.static


class FeatureHandler:
    # Value object for holding handler implementation function and expected handling method
    # So data and  code will be near one another
    # Example usage: FeatureHandler(implementation_function=question_mark, handler=telegram.ext.CommandHandler(["some","data"]))
    def __init__(self) -> None:
        raise NotImplementedError


class SimpleFeatureHandler(FeatureHandler):
    def __init__(
        self,
        func: typing.Callable,
        handler: typing.Callable[..., telegram.ext.Handler],
        command: typing.Union[None, telegram.BotCommand] = None,
    ) -> None:
        self.implementation = func
        self.handler = handler
        self.command = command

    def build(self):
        f = functools.partial(self.implementation)
        self.handler


class FeatureHandlerGroup:
    def __init__(self) -> None:
        pass


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


SimpleFeatureHandler(
    func=version_handler,
    handler=telegram.ext.CommandHandler,
    command=telegram.BotCommand("version", "Show version of the bot."),
    #    context=dict(cmdname="version", additional_data)
)
