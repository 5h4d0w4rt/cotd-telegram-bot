import telegram
import telegram.ext


class DispatcherBuilder:

    def __init__(self, dispatcher: telegram.ext.Dispatcher, **kwargs):
        self.dispatcher = dispatcher

    def with_handlers(self, handlers):
        for handler in handlers:
            self.dispatcher.add_handler(handler)
        return self

    def with_unknown_message_handler(self, unknown_message_handler):
        self.dispatcher.add_handler(unknown_message_handler)
        return self

    def build(self):
        return self.dispatcher
