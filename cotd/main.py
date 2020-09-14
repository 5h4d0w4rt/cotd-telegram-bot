import argparse
import logging
import os
import sys

import cotd.flags
import cotd.handlers
import cotd.logger
import cotd.options
import cotd.updater
import telegram
import telegram.ext
from cotd.flags import parse_feature_flags
from cotd.handlers import (cringe, iscringe, kekw, oldfellow, secret, start, unknown)
from cotd.options import parse_options


def run(updater: telegram.ext.Updater):
    updater.start_polling()
    updater.idle()


def set_bot_commands(updater: telegram.ext.Updater, commands: list):
    updater.bot.set_my_commands(commands)


def set_dispatcher_handlers(updater: telegram.ext.Updater, handlers: list):
    for handler in handlers:
        updater.dispatcher.add_handler(handler)

    updater.dispatcher.add_handler(
        telegram.ext.MessageHandler(telegram.ext.Filters.command, unknown))


def main():
    logger = cotd.logger.get_logger(__name__, logging.DEBUG)
    envs = cotd.updater.EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN'])
    feature_flags = cotd.updater.FeatureFlagsConfig(
        parse_feature_flags(argparse.ArgumentParser(), sys.argv[1:]))
    options = cotd.updater.OptionsConfig(parse_options(argparse.ArgumentParser(), sys.argv[1:]))

    config = cotd.updater.Config(env=envs, features=feature_flags, options=options, logger=logger)

    cotdbot = cotd.updater.COTDBot(config=config)

    set_dispatcher_handlers(cotdbot.updater, [
        telegram.ext.CommandHandler(
            'start', start, filters=~telegram.ext.Filters.update.edited_message),
        telegram.ext.CommandHandler('cringe', cringe),
        telegram.ext.CommandHandler('iscringe', iscringe),
        telegram.ext.CommandHandler('oldfellow', oldfellow),
        telegram.ext.CommandHandler('kekw', kekw),
        telegram.ext.CommandHandler('secret', secret),
    ])

    set_bot_commands(cotdbot.updater, [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("cringe", "Gets you a nice smiley-cat"),
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "Starina siebi nahui"),
        telegram.BotCommand("kekw", "KEKW"),
        telegram.BotCommand("secret", "what's in there?")
    ])

    run(cotdbot.updater)


if __name__ == "__main__":

    main()
