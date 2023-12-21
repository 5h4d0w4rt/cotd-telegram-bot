import pathlib
import subprocess
import typing
import uuid

import requests
import telegram
import telegram.ext

from v1.cotd.plugins.helpers import logged_context


def _youtubedl_impl(url: str):
    result = subprocess.run(["youtube-dl", url, "-o", "%(title)s.%(ext)s"])
    result.check_returncode()


def youtubedl(update: telegram.Update, context: telegram.ext.CallbackContext):
    out = pathlib.Path("temp.mp4")

    _youtubedl_impl(update.effective_message.text, out)

    context.bot.send_video(chat_id=update.effective_chat.id, video=open(out, "rb"))

    out.unlink()
