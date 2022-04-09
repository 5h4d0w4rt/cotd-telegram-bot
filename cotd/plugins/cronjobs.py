import datetime
import typing
import uuid
from cotd.static import Static, StaticReader

import telegram
import telegram.ext

import cotd

def you_made_it(context: telegram.ext.CallbackContext):
    context.bot.send_video_note(chat_id=context.dispatcher._cotd_db,
    video_note=context.bot.static_content.doge_friday
    )

def list_cronjobs(update: telegram.Update,
    context: telegram.ext.CallbackContext):
    jobs = '\n'.join(f"<code>{job.name}: \n {job.job} \n></code>" for job in context.dispatcher.job_queue.jobs())
    return context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = jobs
    )