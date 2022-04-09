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


def _webm_converter_handler_impl(
    download_link: str,
) -> pathlib.Path | subprocess.CalledProcessError:

    # https://some/video.webm
    dl_video_link: str = download_link

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
        dl_video_path.unlink()
        converted_video_path.unlink(missing_ok=True)
        raise
    finally:
        dl_video_path.unlink()

    match type(status):
        case subprocess.CalledProcessError:
            return status
        case _:
            return converted_video_path


@logged_context
def webm_converter_handler(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> typing.Union[telegram.Message, None]:

    converted_video = _webm_converter_handler_impl(update.effective_message.text)
    match type(converted_video):
        case subprocess.CalledProcessError:
            return context.bot.send_message(
                chat_id=context.dispatcher._cotd_db,
                text=f"FFMpeg run failed -- {repr(converted_video)}",
            )
        case _:
            context.bot.send_video(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                video=open(converted_video, "rb"),
            ),

            converted_video.unlink()


def webm_to_mp4(
    ins: pathlib.Path, outs: pathlib.Path
) -> subprocess.CompletedProcess | subprocess.CalledProcessError:
    def _ffmpeg_runner(
        inputfile: pathlib.Path, outputfile: pathlib.Path
    ) -> subprocess.CompletedProcess:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", inputfile, outputfile],
            check=True,
            timeout=180,
            text=True,
            stderr=subprocess.STDOUT,
        )
        return result

    try:
        result = _ffmpeg_runner(ins, outs)
    except subprocess.CalledProcessError as failed_run:
        return failed_run
    except subprocess.TimeoutExpired:
        raise
    return result


@logged_context
def webm_to_mp4_inline(
    update: telegram.Update,
    context: telegram.ext.CallbackContext,
) -> bool:
    """create old fellow result in inline mode"""

    query = update.inline_query.query

    if query == "":
        return update.inline_query.answer([])

    converted_video = _webm_converter_handler_impl(query)

    video = context.bot.send_video(
        chat_id=context.dispatcher._cotd_db, video=open(converted_video, "rb"))

    converted_video.unlink()

    context.bot.delete_message(video.chat_id, video.message_id)

    return context.bot.answer_inline_query(
        inline_query_id=str(uuid.uuid4()),
        results=[
            telegram.InlineQueryResultCachedVideo(
                id=str(uuid.uuid4()),
                title="{query}",
                video_file_id=video.video.file_id,
            )
        ],
    )
