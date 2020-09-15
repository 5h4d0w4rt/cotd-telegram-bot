import argparse
import logging
import os
import re
import sys
import typing
from re import match

import cotd.handlers
import cotd.logger
import cotd.updater
import telegram
import telegram.ext
from cotd.handlers import (cringe, iscringe, kekw, oldfellow, secret, start, unknown)

# class CringeFilter(telegram.ext.BaseFilter):

#     def __init__(self, fileids, metadata):
#         self.fileids = set(fileids)
#         self.metadata = metadata

#     def filter(self, message: telegram.Update) -> bool:
#         try:
#             return (message.reply_to_message.sticker.file_id in self.fileids or
#                     (message.sticker.emoji == '🙂' and
#                      message.sticker.set_name == f'VC_by_{self.metadata.username}'))
#         except AttributeError:
#             return (message.sticker.file_id in self.fileids or
#                     (message.sticker.emoji == '🙂' and
#                      message.sticker.set_name == f'VC_by_{self.metadata.username}'))


def define_feature_flags(parser: argparse.ArgumentParser) -> None:
    pass


def parse_feature_flags(parser: argparse.ArgumentParser,
                        args: typing.List[str]) -> argparse.ArgumentParser:
    return parser.parse_args(args)


def define_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--mode', choices=["token", "webhook"])
    parser.add_argument(
        '--log-level',
        type=lambda x: x.upper(),
        choices=['CRITICAL', 'WARNING', 'ERROR', 'INFO', 'DEBUG'],
        default='ERROR')


def parse_options(parser: argparse.ArgumentParser,
                  args: typing.List[str]) -> argparse.ArgumentParser:
    return parser.parse_args(args)


def run(updater: telegram.ext.Updater) -> None:
    updater.start_polling()
    updater.idle()


def set_bot_commands(updater: telegram.ext.Updater,
                     commands: typing.List[telegram.BotCommand]) -> None:
    updater.bot.set_my_commands(commands)


def set_dispatcher_handlers(updater: telegram.ext.Updater,
                            handlers: typing.List[telegram.ext.Handler]):
    for handler in handlers:
        updater.dispatcher.add_handler(handler)

    updater.dispatcher.add_handler(
        telegram.ext.MessageHandler(telegram.ext.Filters.command, unknown))


def main():
    argparser = argparse.ArgumentParser(description="cringee-bot")
    define_feature_flags(argparser)
    define_options(argparser)
    feature_flags = parse_feature_flags(argparser, sys.argv[1:])
    options = parse_options(argparser, sys.argv[1:])

    envs = cotd.updater.EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN'])

    config = cotd.updater.Config(
        env=envs,
        updater=telegram.ext.Updater(
            token=envs.token,
            use_context=True,
            defaults=telegram.ext.Defaults(
                parse_mode='HTML',
                disable_notification=True,
                disable_web_page_preview=True,
                timeout=5.0,
            )),
        features=feature_flags,
        options=options,
        logger=cotd.logger.get_logger(__name__, level=options.log_level))

    cotdbot = cotd.updater.COTDBot(config)
    cotdbot.logger.info(f"initialized with feature flags: {feature_flags}")
    cotdbot.logger.info(f"initialized with startup options {options}")
    cotdbot.logger.info("initialized config")
    cotdbot.logger.info("initialized cringe of the day client")

    # cringe_filter = CringeFilter(cotdbot.metadata.sticker_set_file_ids, cotdbot.metadata)

    set_dispatcher_handlers(
        cotdbot.updater,
        [
            telegram.ext.CommandHandler(
                'start', start, filters=~telegram.ext.Filters.update.edited_message),
            # telegram.ext.MessageHandler(telegram.ext.Filters.sticker and cringe_filter, iscringe),
            telegram.ext.CommandHandler('iscringe', iscringe),
            telegram.ext.CommandHandler('oldfellow', oldfellow),
            telegram.ext.CommandHandler('kekw', kekw),
            telegram.ext.CommandHandler('secret', secret),
        ])
    cotdbot.logger.info("initialized handlers")

    set_bot_commands(cotdbot.updater, [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "Starina siebi nahui"),
        telegram.BotCommand("kekw", "KEKW"),
        telegram.BotCommand("secret", "what's in there?")
    ])
    cotdbot.logger.info('initialized list of commands')

    run(cotdbot.updater)


if __name__ == "__main__":

    main()
