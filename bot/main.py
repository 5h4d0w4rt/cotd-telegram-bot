from telegram.ext import Updater, Defaults
from telegram.ext import CommandHandler, MessageHandler, Filters
from handlers import unknown, start, cringe, iscringe, oldfellow, kekw, secret
import logging
import os
from config import EnvConfig


def run(updater):
    updater.start_polling()
    updater.idle()


def main(config):
    updater = Updater(token=config.env['token'],
                      use_context=True,
                      defaults=Defaults(
                          parse_mode='HTML',
                          disable_notification=True,
                          disable_web_page_preview=True,
                          timeout=5.0,
                      ))
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start',
                                   start,
                                   filters=~Filters.update.edited_message)
    dispatcher.add_handler(start_handler)

    cringe_handler = CommandHandler('cringe', cringe)
    dispatcher.add_handler(cringe_handler)

    iscringe_handler = CommandHandler('iscringe', iscringe)
    dispatcher.add_handler(iscringe_handler)

    oldfellow_handler = CommandHandler('oldfellow', oldfellow)
    dispatcher.add_handler(oldfellow_handler)

    kekw_handler = CommandHandler('kekw', kekw)
    dispatcher.add_handler(kekw_handler)

    secret_handler = CommandHandler('secret', secret)
    dispatcher.add_handler(secret_handler)
    # must be added last
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.set_my_command()
    run(updater)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    main(EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN']))
