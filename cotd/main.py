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


class CringeFilter(telegram.ext.BaseFilter):

    def __init__(self, fileids, metadata):
        self.fileids = set(fileids)
        self.metadata = metadata

    def filter(self, message: telegram.Update):
        print(message)
        print(self.fileids)
        try:
            return (message.reply_to_message.sticker.file_id in self.fileids or
                    (message.sticker.emoji == '🙂' and
                     message.sticker.set_name == f'VC_by_{self.metadata.username}'))
        except AttributeError:
            return (message.sticker.file_id in self.fileids or
                    (message.sticker.emoji == '🙂' and
                     message.sticker.set_name == f'VC_by_{self.metadata.username}'))


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


def setup_sticker_set(cotdbot: cotd.updater.COTDBot):
    fileids = []
    me = cotdbot.updater.bot.get_me()
    try:
        sticker_pack = cotdbot.updater.bot.get_sticker_set(f"VC_by_{me.username}")
        if sticker_pack:
            fileids.extend(list(sticker.file_id for sticker in sticker_pack.stickers))
    except telegram.error.BadRequest as err:
        if 'Stickerset_invalid' in str(err):
            sticker_pack = cotdbot.updater.bot.create_new_sticker_set(
                png_sticker=open("static/smileyOne512x512.png", 'rb'),
                name=f"VC_by_{me.username}",
                title=f"VC_by_{me.username}",
                user_id=int(145043750),
                emojis="🙂😊")
            fileids.extend(list(sticker.file_id for sticker in sticker_pack.stickers))
        else:
            raise
    cotdbot.config.logger.info(fileids)
    return fileids


def main():
    logger = cotd.logger.get_logger(__name__, logging.DEBUG)
    envs = cotd.updater.EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN'])
    logger.info("initialized environment variables")
    feature_flags = parse_feature_flags(argparse.ArgumentParser(), sys.argv[1:])
    logger.info(f"initialized feature flags: {feature_flags}")
    options = parse_options(argparse.ArgumentParser(), sys.argv[1:])
    logger.info(f"initialized startup options {options}")
    config = cotd.updater.Config(env=envs, features=feature_flags, options=options, logger=logger)
    logger.info("initialized config")
    cotdbot = cotd.updater.COTDBot(config=config)
    logger.info("initialized cringe of the day client")
    fileids = setup_sticker_set(cotdbot)

    cringe_filter = CringeFilter(fileids, cotdbot.updater.bot.get_me())

    set_dispatcher_handlers(cotdbot.updater, [
        telegram.ext.CommandHandler(
            'start', start, filters=~telegram.ext.Filters.update.edited_message),
        telegram.ext.CommandHandler('cringe', cringe),
        telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'iscringe|😊|🙂'), iscringe),
        telegram.ext.MessageHandler(telegram.ext.Filters.sticker and cringe_filter, iscringe),
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
