from cotd.plugins.helpers import logged_context
import telegram
import telegram.ext
import random
import typing


@logged_context
def voice_reaction(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> telegram.Message:
    voice_messages = [
        "как болезнь называется?",
        "пацаны, тут человеку руки оторвало!",
        "слова красивые, но ты пидор",
        "ничего не понял",
        "не могу послушать твоё голосове, мне оторвало уши",
        "пиши давай",
    ]
    if random.randint(0, 5) != 3:
        msg = voice_messages[random.randint(0, len(voice_messages) - 1)]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            reply_to_message_id=update.message.message_id,
            text=msg,
        )

    return context.bot.sendSticker(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.effective_message.message_id,
        sticker="CAACAgIAAxkBAAIBy2DHu6uTHF_uKSwtLRuWcUmHNHejAAI-AQAC39LPAoZ3xK3gRdEhHwQ",
    )
