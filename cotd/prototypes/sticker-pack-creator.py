# createNewStickerSet
import cotd.updater
from cotd.updater import EnvConfig
import os


def run(cotdbot: cotd.updater.COTDBot):
    cotdbot.updater.start_polling()
    cotdbot.updater.idle()


def main():
    config = cotd.updater.Config(env=EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN']))
    cotdbot = cotd.updater.COTDBot(config)
    run(cotdbot)


if __name__ == "__main__":
    main()
