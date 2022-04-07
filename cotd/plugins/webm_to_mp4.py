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

    # https://some/video.webm
    dl_video_link: str = update.effective_message.text

    # video.webm
    dl_video_name = dl_video_link.rsplit("/")[-1]

    # video.mp4
    converted_video_name = f"{dl_video_name.split('.')[0]}.mp4"

    # /tmp/video.webm
    dl_video_path = pathlib.Path(f"/tmp/{dl_video_name}")

    # /tmp/video.mp4
    converted_video_path = pathlib.Path(f"/tmp/{converted_video_name}")

    with open(f"{dl_video_path}", "wb") as dl_video_file:
        dl_video_file.write(requests.get(dl_video_link, allow_redirects=True).content)

    try:
        status = webm_to_mp4(dl_video_path, converted_video_path)
    except Exception as err:
        raise
    finally:
        if status != 0:
            print(err)
        dl_video_path.unlink()

    return converted_video_path


@logged_context
def webm_converter_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    converted_video = _webm_converter_handler_impl(update, context)
    context.bot.send_video(
        chat_id=update.effective_chat.id,
        reply_to_message_id=update.message.message_id,
        video=open(pathlib.Path(converted_video), "rb"),
    )
    converted_video.unlink()
