import argparse
import logging
import os
from re import match
import sys
import re
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
    logger.info("initialized environment variables")
    feature_flags = cotd.updater.FeatureFlagsConfig(
        parse_feature_flags(argparse.ArgumentParser(), sys.argv[1:]))
    logger.info("initialized feature flags")
    options = cotd.updater.OptionsConfig(parse_options(argparse.ArgumentParser(), sys.argv[1:]))
    logger.info("initialized startup options")
    config = cotd.updater.Config(env=envs, features=feature_flags, options=options, logger=logger)
    logger.info("initialized config")
    cotdbot = cotd.updater.COTDBot(config=config)
    logger.info("initialized cringe of the day client")
    set_dispatcher_handlers(cotdbot.updater, [
        telegram.ext.CommandHandler(
            'start', start, filters=~telegram.ext.Filters.update.edited_message),
        telegram.ext.CommandHandler('cringe', cringe),
        telegram.ext.PrefixHandler(['!', '#'], ['iscringe', "😊", "🙂"], iscringe),
        telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'iscringe|😊|🙂'), iscringe),
        telegram.ext.CommandHandler('iscringe', iscringe),
        telegram.ext.CommandHandler('oldfellow', oldfellow),
        telegram.ext.CommandHandler('kekw', kekw),
        telegram.ext.CommandHandler('secret', secret),
    ])
    logger.info("initialized handlers")
    set_bot_commands(cotdbot.updater, [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("cringe", "Gets you a nice smiley-cat"),
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "Starina siebi nahui"),
        telegram.BotCommand("kekw", "KEKW"),
        telegram.BotCommand("secret", "what's in there?")
    ])
    logger.info('initialized list of commands')
    run(cotdbot.updater)


if __name__ == "__main__":

    main()
