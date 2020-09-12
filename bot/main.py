from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from handlers import unknown, start, cringe, oldfellow, kekw
import logging
import os
from config import Config


def run(updater):
    updater.start_polling()


def main(config):
    updater = Updater(token=config.env['token'], use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    cringe_handler = CommandHandler('cringe', cringe)
    dispatcher.add_handler(cringe_handler)

    oldfellow_handler = CommandHandler('oldfellow', oldfellow)
    dispatcher.add_handler(oldfellow_handler)

    kekw_handler = CommandHandler('kekw', kekw)
    dispatcher.add_handler(kekw_handler)
    # must be added last
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    run(updater)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    main(Config(token=os.environ['COTD_TELEGRAM_BOT_TOKEN']))
