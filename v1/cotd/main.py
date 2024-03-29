import argparse
import datetime
import functools
import os
import re

import telegram
import telegram.ext
from zoneinfo import ZoneInfo

import v1.cotd.cacher
import v1.cotd.logger
import v1.cotd.service
import v1.cotd.static
import v1.cotd.storage
from v1.cotd.plugins.cringelord import cringelord
from v1.cotd.plugins.cronjobs import cronjobsctl, you_made_it
from v1.cotd.plugins.helpers import check_chance, check_timer
from v1.cotd.plugins.inliner import menu
from v1.cotd.plugins.kandinsky import kandinsky_handler
from v1.cotd.plugins.misc import (
    bot_reaction,
    cuno_handler,
    games_reaction,
    goaway,
    grass_reaction,
    gym_reaction,
    iscringe,
    journalism_reaction,
    kekw,
    leftie_meme_detector,
    massacre_reaction,
    music_reaction,
    no_reaction,
    patriot_reaction,
    pig_reaction,
    question_mark,
    stuffy_reaction,
    trista_reaction,
    tweet_reaction,
    voice_reaction,
    watermelon_reaction,
    yes_reaction,
)
from v1.cotd.plugins.prospector import cache_users
from v1.cotd.plugins.security import check_allowed_sources
from v1.cotd.plugins.webm_to_mp4 import webm_converter_handler
from v1.cotd.plugins.youtuber import youtubedl

TZ = ZoneInfo("Europe/Moscow")
# a regular expression that matches news from blacklist.
re_news_blacklist = re.compile(r".*meduza\.io.*|.*lenta\.ru.*|.*vc\.ru.*", re.IGNORECASE)
# a regular expression that matches news from blacklist.
re_news_whitelist = re.compile(r".*rt_russian.*", re.IGNORECASE)
# a regular expression that matches gym.
re_gym = re.compile(r".*качалк.*", re.IGNORECASE)
# a regular expression that matches stuffy words.
re_stuffy_handler = re.compile(r".*душ(ный|нила|но|ишь|ара).*", re.IGNORECASE)
# piggy
re_piggy = re.compile(r".*хрю.*", re.IGNORECASE)
# watermelon
re_watermelon = re.compile(r".*(а|a)(р|p)б(у|y)з.*", re.IGNORECASE)
# 300
re_300 = re.compile(r".* 300 .*|.* триста .*|^300$|^300 .*|^триста$|^триста .*", re.IGNORECASE)
# massacre
re_massacre = re.compile(r".*резня.*", re.IGNORECASE)
# spotify
re_spotify = re.compile(r".*open\.spotify\.com.*", re.IGNORECASE)
# Fuck does Cuno care?
re_cuno = re.compile(r"похуй|мне похуй", re.IGNORECASE)
# It's me!
re_bot = re.compile(r".* бот(|а|у) .*|^бо(т|та|ту).*", re.IGNORECASE)
# oh shit, i'm sorry!
re_gacha = re.compile(r".* гач(|а|у|и) .*|^гач(а|у|и).*", re.IGNORECASE)
# links with webm
re_webm_link = re.compile(r"http.*:\/\/.*.webm", re.IGNORECASE)
# youtube link
re_youtube_link = re.compile(r"http.*:\/\/.*(youtube.com|youtu.be)", re.IGNORECASE)
# tweet
re_tweet = re.compile(r".*twitter\.com.*", re.IGNORECASE)
# gamers
re_games = re.compile(r".* глум .*|^глум.*", re.IGNORECASE)


# not used yet
class ThrottleFilter(telegram.ext.UpdateFilter):
    def filter(self, update: telegram.Update):
        return


# not used yet
class ChanceFilter(telegram.ext.UpdateFilter):
    def filter(self, update: telegram.Update):
        return


def next_date(given_date: datetime.date, weekday: int) -> datetime.date:
    # https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-date
    day_shift = (weekday - given_date.weekday()) % 7
    return given_date + datetime.timedelta(days=day_shift)


def date_to_datetime(d: datetime.date, tz=None) -> datetime.datetime:
    return datetime.datetime.combine(d, datetime.datetime.min.time(), tzinfo=tz)


def define_feature_flags(parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
    flags = parser.add_argument_group("flags")
    flags.add_argument("--feature-enable-security", action="store_true", default=False)
    flags.add_argument("--feature-enable-persistence", action="store_true", default=False)
    flags.add_argument("--feature-enable-webm-converter", action="store_true", default=False)
    flags.add_argument("--feature-enable-youtubedl", action="store_true", default=False)
    return flags


def define_options(parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
    options = parser.add_argument_group("options")
    options.add_argument("--mode", choices=["token", "webhook"])
    options.add_argument("--version")
    options.add_argument(
        "--log-level",
        type=lambda x: x.upper(),
        choices=["CRITICAL", "WARNING", "ERROR", "INFO", "DEBUG"],
        default="ERROR",
    )
    options.add_argument("--group")
    options.add_argument("--db")  # chat group that work as a database
    return options


def main():
    argparser = argparse.ArgumentParser(description="cringee-bot")

    _flags = define_feature_flags(argparser)
    _options = define_options(argparser)
    args = argparser.parse_args()

    features = v1.cotd.service.Flags(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _flags._group_actions)
        }
    )
    options = v1.cotd.service.Options(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _options._group_actions)
        }
    )

    data = v1.cotd.static.StaticReader(
        v1.cotd.static.Static(
            **dict(
                kekw="static/KEKW.mp4",
                oldfellow="static/oldfellow.mp4",
                ribnikov="static/ribnikov.based.mp4",
                sniff_dog="static/cringe-sniff-dog.jpg",
                stuffy="static/stuffy.jpg",
                music="static/music.jpg",
                journalism="static/journalism.jpg",
                sf="static/deadinside.jpg",
                go_away="static/go_away.mp4",
                doge_friday="static/doge_friday.mp4",
            )
        )
    )

    cache = v1.cotd.cacher.MediaCacheInMemory()

    handlers = [
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": -100,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.all,
                        functools.partial(
                            check_allowed_sources,
                            trusted_sources=dict(users="All", chats=[int(options.group), int(options.db)]),
                        ),
                    ),
                ]
                if features.feature_enable_security is True
                else [],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": -99,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text,
                        functools.partial(cache_users),
                    ),
                ],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": -98,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_webm_link),
                        functools.partial(webm_converter_handler),
                    ),
                ]
                if features.feature_enable_webm_converter
                else [],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": -97,
                "handlers": [
                    telegram.ext.MessageHandler(telegram.ext.Filters.regex(re_youtube_link), youtubedl),
                ]
                if features.feature_enable_youtubedl
                else [],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": 1,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.voice,
                        functools.partial(voice_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.photo,
                        functools.partial(kandinsky_handler),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_news_blacklist),
                        functools.partial(journalism_reaction, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_news_whitelist),
                        functools.partial(patriot_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_gym),
                        functools.partial(gym_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_tweet),
                        functools.partial(tweet_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_stuffy_handler),
                        functools.partial(stuffy_reaction, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_spotify),
                        functools.partial(music_reaction, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_bot),
                        functools.partial(bot_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text(["?", "??", "???"]),
                        functools.partial(question_mark),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text(["Нет.", "Нет", "нет", "нет."]),
                        functools.partial(no_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text(["Да.", "Да", "да", "да."]),
                        functools.partial(yes_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_gacha),
                        functools.partial(grass_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_games),
                        functools.partial(games_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_piggy),
                        functools.partial(pig_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_watermelon),
                        functools.partial(watermelon_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_massacre),
                        functools.partial(massacre_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_300),
                        functools.partial(trista_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_cuno),
                        functools.partial(cuno_handler, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text,
                        functools.partial(leftie_meme_detector),
                    ),
                ],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": 2,
                "handlers": [
                    telegram.ext.CommandHandler(
                        "iscringe", functools.partial(iscringe, data=data, cache=cache)
                    ),
                    telegram.ext.CommandHandler(
                        "cringelord",
                        functools.partial(cringelord, data=data, cache=cache),
                    ),
                    telegram.ext.CommandHandler("goaway", functools.partial(goaway, data=data, cache=cache)),
                    telegram.ext.CommandHandler("kekw", functools.partial(kekw, data=data, cache=cache)),
                    telegram.ext.CommandHandler(
                        "jobs",
                        functools.partial(cronjobsctl),
                        filters=telegram.ext.Filters.chat(int(options.db)),
                    ),
                    telegram.ext.CommandHandler(
                        "config",
                        lambda update, context: print(),
                        filters=telegram.ext.Filters.chat(int(options.db)),
                    ),
                ],
            }
        ),
        v1.cotd.service.HandlerGroup(
            **{
                "group_index": 3,
                "handlers": [telegram.ext.InlineQueryHandler(functools.partial(menu, data=data))],
            }
        ),
    ]

    commands = [
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("goaway", "Helpful reminder to go on your business"),
        telegram.BotCommand("cringelord", "Who's cringelord of the day?"),
        telegram.BotCommand("kekw", "E TU BRUTE? :DDD"),
        telegram.BotCommand("jobs", "Show scheduled jobs"),
        telegram.BotCommand("config", "Show options/features"),
    ]

    cotdbot = v1.cotd.service.factory(
        envs=v1.cotd.service.EnvConfig(token=os.environ["COTD_TELEGRAM_BOT_TOKEN"]),
        features=features,
        options=options,
        client_logger=v1.cotd.logger.get_logger("TGBotClient", level=options.log_level),
        cotd_logger=v1.cotd.logger.get_logger("COTDBotService", level=options.log_level),
        handlers=handlers,
        commands=commands,
        storage=v1.cotd.storage.TelegramSavedMessagesStorage(db=options.db),
        static_content=data,
    )

    cotdbot.logger.info(f"initialized with feature flags: {features}")
    cotdbot.logger.info(f"initialized with startup options {options}")

    cotdbot.client.initialize()

    # register jobs block

    cotdbot.client.updater.job_queue.run_repeating(
        you_made_it,
        interval=datetime.timedelta(days=7),
        first=date_to_datetime(next_date(datetime.date.today(), 4), tz=TZ),
    )

    cotdbot.logger.info("initialized cringe of the day client")

    cotdbot.client.run()


if __name__ == "__main__":
    main()
