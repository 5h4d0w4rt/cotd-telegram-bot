import argparse
import logging
import os
import sys

import cotd_bot.builders
import cotd_bot.flags
import cotd_bot.handlers
import cotd_bot.logger
import cotd_bot.options
import cotd_bot.updater
import telegram
import telegram.ext
from cotd_bot.flags import parse_feature_flags
from cotd_bot.handlers import (cringe, iscringe, kekw, oldfellow, secret, start,
                               unknown)
from cotd_bot.logger import logger
from cotd_bot.options import parse_options


def run(updater: telegram.ext.Updater):
    updater.start_polling()
    updater.idle()


def init_set_commands(updater: telegram.ext.Updater, commands: list):
    updater.bot.set_my_commands(commands)


def init_dispatcher(updater: telegram.ext.Updater, handlers: list):
    cotd_bot.builders.DispatcherBuilder(updater.dispatcher).with_handlers(
        handlers).with_unknown_message_handler(
            telegram.ext.MessageHandler(telegram.ext.Filters.command,
                                        unknown)).build()


def main():
    config = cotd_bot.updater.Config(
        env=cotd_bot.updater.EnvConfig(
            token=os.environ['COTD_TELEGRAM_BOT_TOKEN']),
        features=cotd_bot.updater.FeatureFlagsConfig(
            features=parse_feature_flags(argparse.ArgumentParser(),
                                         sys.argv[1:])),
        options=cotd_bot.updater.OptionsConfig(
            options=parse_options(argparse.ArgumentParser(), sys.argv[1:])),
        logger=logger(__name__, logging.DEBUG))

    cotd = cotd_bot.updater.COTDBot(config=config)

    handlers = [
        telegram.ext.CommandHandler(
            'start', start,
            filters=~telegram.ext.Filters.update.edited_message),
        telegram.ext.CommandHandler('cringe', cringe),
        telegram.ext.CommandHandler('iscringe', iscringe),
        telegram.ext.CommandHandler('oldfellow', oldfellow),
        telegram.ext.CommandHandler('kekw', kekw),
        telegram.ext.CommandHandler('secret', secret),
    ]

    commands = [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("cringe", "Gets you a nice smiley-cat"),
        telegram.BotCommand(
            "iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "Starina siebi nahui"),
        telegram.BotCommand("kekw", "KEKW"),
        telegram.BotCommand("secret", "what's in there?")
    ]

    init_dispatcher(cotd.updater, handlers)
    init_set_commands(cotd.updater, commands)

    run(cotd.updater)


if __name__ == "__main__":

    main()
