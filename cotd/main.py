import argparse
import logging
import os
import typing
import functools
import re
import types
import telegram
import telegram.ext

import cotd.static
import cotd.logger
import cotd.service
import cotd.cacher
import cotd.storage

from cotd.handlers import (
    cache_users,
    leftie_meme_detector,
    start,
    voice_reaction,
    question_mark,
    no_reaction,
    yes_reaction,
    manet_reaction,
    pig_reaction,
    stuffy_handler,
    journalism_handler,
    gym_reaction,
    cringelord,
    kekw,
    oldfellow,
    goaway,
    secret,
    iscringe,
    motivation_handler_v1,
    watermelon_reaction,
    trista_reaction,
    massacre_reaction,
    music_handler,
    dead_inside_handler,
    version_handler,
)

from cotd.plugins.motivationv2 import motivation_handler_v2

# a regular expression that matches news from blacklist.
re_news_blacklist = re.compile(r".*meduza\.io.*|.*lenta\.ru.*|.*vc\.ru.*", re.IGNORECASE)
# a regular expression that matches gym.
re_gym = re.compile(r".*качалк.*", re.IGNORECASE)
# a regular expression that matches stuffy words.
re_stuffy_handler = re.compile(r".*душ(ный|нила|но|ишь|ара).*", re.IGNORECASE)
# piggy
re_piggy = re.compile(r".*хрю.*", re.IGNORECASE)
# watermelon
re_watermelon = re.compile(r".*арбуз.*", re.IGNORECASE)
# 300
re_300 = re.compile(r".* 300 .*|.* триста .*|^300$|^300 .*|^триста$|^триста .*", re.IGNORECASE)
# massacre
re_massacre = re.compile(r".*резня.*", re.IGNORECASE)
# music
re_music = re.compile(r".*open.spotify.com.*", re.IGNORECASE)
# dead inside
re_dead_inside = re.compile(r"похуй|мне похуй", re.IGNORECASE)


def define_feature_flags(parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
    flags = parser.add_argument_group("flags")
    flags.add_argument("--enable-persistence", action="store_true", default=False)
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
    return options


def main():
    argparser = argparse.ArgumentParser(description="cringee-bot")

    _flags = define_feature_flags(argparser)
    _options = define_options(argparser)
    args = argparser.parse_args()

    features = cotd.service.Flags(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _flags._group_actions)
        }
    )
    options = cotd.service.Options(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _options._group_actions)
        }
    )

    data = cotd.static.StaticReader(
        cotd.static.Static(
            files=types.MappingProxyType(
                dict(
                    kekw="static/KEKW.mp4",
                    oldfellow="static/oldfellow.mp4",
                    ribnikov="static/ribnikov.based.mp4",
                    sniff_dog="static/cringe-sniff-dog.jpg",
                    stuffy="static/stuffy.jpg",
                    music="static/music.jpg",
                    journalism="static/journalism.jpg",
                    sf="static/deadinside.jpg",
                    go_away="static/go_away.mp4",
                )
            )
        )
    )

    cache = cotd.cacher.MediaCacheInMemory()

    handlers = [
        cotd.service.HandlerGroup(
            **{
                "group_index": 0,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text,
                        functools.partial(cache_users, cache=cache),
                    ),
                ],
            }
        ),
        cotd.service.HandlerGroup(
            **{
                "group_index": 1,
                "handlers": [
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.voice,
                        functools.partial(voice_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.photo,
                        functools.partial(manet_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_news_blacklist),
                        functools.partial(journalism_handler, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_gym),
                        functools.partial(gym_reaction),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_stuffy_handler),
                        functools.partial(stuffy_handler, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.regex(re_music),
                        functools.partial(music_handler, data=data, cache=cache),
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
                        telegram.ext.Filters.regex(re_dead_inside),
                        functools.partial(dead_inside_handler, data=data, cache=cache),
                    ),
                    telegram.ext.MessageHandler(
                        telegram.ext.Filters.text,
                        functools.partial(leftie_meme_detector),
                    ),
                ],
            }
        ),
        cotd.service.HandlerGroup(
            **{
                "group_index": 2,
                "handlers": [
                    telegram.ext.CommandHandler(
                        "start",
                        start,
                        filters=~telegram.ext.Filters.update.edited_message,
                    ),
                    telegram.ext.CommandHandler("version", functools.partial(version_handler)),
                    telegram.ext.CommandHandler(
                        "iscringe", functools.partial(iscringe, data=data, cache=cache)
                    ),
                    telegram.ext.CommandHandler(
                        "oldfellow",
                        functools.partial(oldfellow, data=data, cache=cache),
                    ),
                    telegram.ext.CommandHandler(
                        "cringelord",
                        functools.partial(cringelord, data=data, cache=cache),
                    ),
                    telegram.ext.CommandHandler(
                        "goaway", functools.partial(goaway, data=data, cache=cache)
                    ),
                    telegram.ext.CommandHandler(
                        "kekw", functools.partial(kekw, data=data, cache=cache)
                    ),
                    telegram.ext.CommandHandler(
                        "secret", functools.partial(secret, data=data, cache=cache)
                    ),
                    telegram.ext.CommandHandler(
                        "motivationv1", functools.partial(motivation_handler_v1)
                    ),
                ],
            }
        ),
        cotd.service.HandlerGroup(
            **{
                "group_index": 3,
                "handlers": [
                    telegram.ext.InlineQueryHandler(functools.partial(motivation_handler_v2))
                ],
            }
        ),
    ]

    commands = [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("version", "Show version of the bot."),
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "oldfellow, take off!"),
        telegram.BotCommand("goaway", "Helpful reminder to go on your business"),
        telegram.BotCommand("cringelord", "Who's cringelord of the day?"),
        telegram.BotCommand("kekw", "E TU BRUTE? :DDD"),
        telegram.BotCommand("motivation", "get motivation! example: /motivation text"),
        telegram.BotCommand("secret", "what's in there?"),
    ]

    envs = cotd.service.EnvConfig(token=os.environ["COTD_TELEGRAM_BOT_TOKEN"])

    cotdbot = cotd.service.factory(
        envs=envs,
        features=features,
        options=options,
        client_logger=cotd.logger.get_logger("TGBotClient", level=options.log_level),
        cotd_logger=cotd.logger.get_logger("COTDBotService", level=options.log_level),
        handlers=handlers,
        commands=commands,
        storage=cotd.storage.TelegramSavedMessagesStorage(),
    )

    cotdbot.logger.info(f"initialized with feature flags: {features}")
    cotdbot.logger.info(f"initialized with startup options {options}")

    cotdbot.client.initialize()

    cotdbot.logger.info("initialized cringe of the day client")

    cotdbot.client.run()


if __name__ == "__main__":

    main()
