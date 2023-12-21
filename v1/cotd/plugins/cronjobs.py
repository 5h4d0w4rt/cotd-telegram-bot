import datetime
import typing
import uuid

import ratelimit
import telegram
import telegram.ext

import v1.cotd
from v1.cotd.static import Static, StaticReader


def you_made_it(context: telegram.ext.CallbackContext):
    context.bot.send_video_note(
        chat_id=context.dispatcher._cotd_group, video_note=context.bot.static_content.doge_friday
    )


# TODO remake in ctl keyboard
def cronjobsctl(update: telegram.Update, context: telegram.ext.CallbackContext):
    ctl = update.effective_message.text.removeprefix("/jobs").strip()

    jobs = "\n".join(
        f"<code>run:{job.name}</code>: \n {job.job} \n" for job in context.dispatcher.job_queue.jobs()
    )

    match ctl:
        case "help":
            return
        case "list":
            return context.bot.send_message(chat_id=update.effective_chat.id, text=jobs)
        case "run:you_made_it" as run_cmd:
            context.dispatcher.job_queue.get_jobs_by_name(run_cmd.split(":")[-1])[0].run(context.dispatcher)
