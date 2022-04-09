import datetime
import typing
import uuid
from cotd.static import Static, StaticReader
import ratelimit
import telegram
import telegram.ext

import cotd


def you_made_it(context: telegram.ext.CallbackContext):
    context.bot.send_video_note(
        chat_id=context.dispatcher._cotd_db, video_note=context.bot.static_content.doge_friday
    )

# TODO remake in ctl keyboard
def cronjobsctl(update: telegram.Update, context: telegram.ext.CallbackContext):
    ctl = update.effective_message.text.removeprefix("/jobs").strip()

    jobs = "\n".join(
        f"<code>{job.name}: \n {job.job} \n></code>" for job in context.dispatcher.job_queue.jobs()
    )

    match ctl:
        case "list":
            return context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)
        case "run:doge":
            context.dispatcher.job_queue.get_jobs_by_name("you_made_it")[0].run(context.dispatcher)
