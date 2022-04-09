from asyncio import subprocess
from importlib.resources import path
import pathlib
import subprocess
from cotd.plugins.helpers import logged_context
import telegram
import telegram.ext
import typing
import requests

import uuid

def _youtubedl_impl(url: str, outfile: pathlib.Path):
    result = subprocess.run(['youtube-dl', url, '-o', outfile])
    result.check_returncode()

def youtubedl(update: telegram.Update,
    context: telegram.ext.CallbackContext):

    out = pathlib.Path('temp.mp4')

    _youtubedl_impl(update.effective_message.text, out)

    context.bot.send_video(chat_id=update.effective_chat.id, video=open(out, 'rb'))

    out.unlink()