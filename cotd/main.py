import argparse
import logging
import os
import typing
import functools
import cotd.logger
import cotd.service
import cotd.cacher
from cotd.handlers import cache_users, start, cringelord, kekw, oldfellow, goaway, secret, iscringe
import cotd.static
from cotd.service import TGBotMetadata

import telegram
import telegram.ext


class Options(argparse.Namespace):
    pass


class Flags(argparse.Namespace):
    pass


def define_feature_flags(parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
    flags = parser.add_argument_group("flags")
    flags.add_argument("--stub-feature-flag")
    return flags


def define_options(parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
    options = parser.add_argument_group("options")
    options.add_argument("--mode", choices=["token", "webhook"])
    options.add_argument(
        "--log-level",
        type=lambda x: x.upper(),
        choices=["CRITICAL", "WARNING", "ERROR", "INFO", "DEBUG"],
        default="ERROR",
    )
    options.add_argument("--group")
    return options


def cotd_service_factory(
    envs: cotd.service.EnvConfig,
    features: Flags,
    options: Options,
    logger: logging.Logger,
    commands: typing.List[telegram.BotCommand],
    handlers: typing.List[cotd.service.HandlerGroup],
) -> cotd.service.COTDBotService:

    updater = telegram.ext.Updater(
        token=envs.token,
        use_context=True,
        defaults=telegram.ext.Defaults(
            parse_mode="HTML",
            disable_notification=True,
            disable_web_page_preview=True,
            timeout=5.0,
        ),
    )

    metadata = TGBotMetadata(updater.bot.get_me())

    logger.setLevel(options.log_level)

    updater.logger.setLevel(options.log_level)
    updater.logger.addHandler(logging.StreamHandler())

    updater.dispatcher.logger.setLevel(options.log_level)
    updater.dispatcher.logger.addHandler(logging.StreamHandler())

    config = cotd.service.COTDBotConfig(
        env=envs,
        updater=updater,
        features=features,
        options=options,
        logger=logger,
        metadata=metadata,
        handlers=handlers,
        commands=commands,
    )

    cotdbot = cotd.service.COTDBotService(config)
    return cotdbot


def main():
    argparser = argparse.ArgumentParser(description="cringee-bot")

    _flags = define_feature_flags(argparser)
    _options = define_options(argparser)
    args = argparser.parse_args()

    features = Flags(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _flags._group_actions)
        }
    )
    options = Options(
        **{
            name: value
            for (name, value) in args._get_kwargs()
            if name in set(y.dest for y in _options._group_actions)
        }
    )

    data = cotd.static.STATIC
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
                    telegram.ext.CommandHandler(
                        "start",
                        start,
                        filters=~telegram.ext.Filters.update.edited_message,
                    ),
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
                        "secret", functools.partial(secret, data=data)
                    ),
                ],
            }
        ),
    ]

    commands = [
        telegram.BotCommand("start", "Hello world"),
        telegram.BotCommand("iscringe", "Determines if post you reply to is cringe or based"),
        telegram.BotCommand("oldfellow", "oldfellow, take off!"),
        telegram.BotCommand("goaway", "Helpful reminder to go on your business"),
        telegram.BotCommand("cringelord", "Who's cringelord of the day?"),
        telegram.BotCommand("kekw", "E TU BRUTE? :DDD"),
        telegram.BotCommand("secret", "what's in there?"),
    ]

    envs = cotd.service.EnvConfig(token=os.environ["COTD_TELEGRAM_BOT_TOKEN"])

    cotdbot = cotd_service_factory(
        envs=envs,
        features=features,
        options=options,
        logger=cotd.logger.get_logger("COTDBotService", level=options.log_level),
        handlers=handlers,
        commands=commands,
    )

    cotdbot.logger.info(f"initialized with feature flags: {features}")
    cotdbot.logger.info(f"initialized with startup options {options}")

    cotdbot.initialize()

    cotdbot.logger.info("initialized cringe of the day client")

    cotdbot.run()


if __name__ == "__main__":

    main()
