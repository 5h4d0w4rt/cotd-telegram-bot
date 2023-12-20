import datetime
import typing

import telegram
import telegram.ext

from cotd.cacher import MediaCache


def cache_users(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> None:
    user: telegram.User = update.effective_user
    chat: telegram.Chat = update.effective_chat

    today = datetime.datetime.now()
    today = today.strftime("%d-%m-%Y")

    if not context.user_data.get(user.id):
        context.user_data[user.id] = user.to_dict()
        context.user_data[user.id].setdefault("messages", {today: 1})
    else:
        context.user_data[user.id]["messages"].setdefault(today, 0)
        context.user_data[user.id]["messages"][today] += 1

    if chat:
        if not context.chat_data.get(user.id):
            context.chat_data[user.id] = user.to_dict()
            context.chat_data[user.id].setdefault("messages", {today: 1})
        else:
            context.chat_data[user.id]["messages"].setdefault(today, 0)
            context.chat_data[user.id]["messages"][today] += 1

    context.dispatcher.logger.debug(context.user_data)
    context.dispatcher.logger.debug(context.chat_data)
    context.dispatcher.logger.debug(update.effective_user)
