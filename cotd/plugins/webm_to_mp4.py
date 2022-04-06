from importlib.resources import path
import pathlib
from cotd.plugins.helpers import logged_context
from cotd.utils import webm_to_mp4
import telegram
import telegram.ext
import typing
import requests


def _webm_converter_handler_impl(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> pathlib.Path:

    dl_video_link: str = update.effective_message.text

    dl_video_name = dl_video_link.rsplit("/")[-1]
    converted_video_name = f"{dl_video_name.split('.')[0]}.mp4"

    dl_video_path = pathlib.Path(f"/tmp/{dl_video_name}")
    converted_video_path = pathlib.Path(f"/tmp/{converted_video_name}")

    x = requests.get(dl_video_link, allow_redirects=True)
    with open(f"{dl_video_path}", "wb") as dl_video_file:
        dl_video_file.write(requests.get(dl_video_link, allow_redirects=True).content)

    webm_to_mp4(dl_video_path, converted_video_path)

    return converted_video_path


@logged_context
def webm_converter_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    video = _webm_converter_handler_impl(update, context)

    return context.bot.send_video(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        video=open(pathlib.Path(video), "rb"),
    )
