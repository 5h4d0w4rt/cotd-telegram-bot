# createNewStickerSet
import cotd.updater
from cotd.updater import EnvConfig
import os
import telegram
import telegram.ext


def run(cotdbot: cotd.updater.COTDBot):
    cotdbot.updater.start_polling()
    cotdbot.updater.idle()


def start(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    return context.bot.send_message(chat_id=update.effective_chat.id, text="start")


def main():
    config = cotd.updater.Config(env=EnvConfig(token=os.environ['COTD_TELEGRAM_BOT_TOKEN']))
    cotdbot = cotd.updater.COTDBot(config)
    me = cotdbot.updater.bot.get_me()
    print(me)
    # print(cotdbot.updater.bot.get_sticker_set("VolumetricCringeStickerSet"))
    cotdbot.updater.bot.create_new_sticker_set(
        png_sticker=open("static/ezgif.com-resize.png", 'rb'),
        name=f"VC_by_{me.username}",
        title=f"VC_by_{me.username}",
        user_id=int(me.id),
        emojis="🙂")
    run(cotdbot)


if __name__ == "__main__":
    main()
