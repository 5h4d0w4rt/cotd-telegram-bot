import telegram
import telegram.ext
import logging
import argparse
import typing
from dataclasses import dataclass
import cotd.storage


@dataclass
class Options(argparse.Namespace):
    log_level: str
    version: str
    group: int
    mode: str


@dataclass
class Flags(argparse.Namespace):
    enable_persistence: bool


@dataclass
class EnvConfig:
    token: str


@dataclass
class TGBotMetadata:
    user: typing.Union[telegram.User, None]


@dataclass
class COTDBotStickers:
    sticker_set: telegram.StickerSet
    sticker_set_file_ids: typing.List[str]


@dataclass
class HandlerGroup:
    group_index: int
    handlers: typing.List[telegram.ext.Handler]


@dataclass
class TGBotConfig:
    updater: telegram.ext.Updater
    options: argparse.Namespace
    metadata: TGBotMetadata
    handlers: typing.List[HandlerGroup]
    commands: typing.List[telegram.BotCommand]


@dataclass
class COTDBotConfig:
    features: argparse.Namespace
    logger: logging.Logger


class TGBotClient:
    def __init__(self, config: TGBotConfig):
        self.options = config.options
        self.updater = config.updater
        self.metadata = config.metadata
        self.commands = config.commands
        self.handlers = config.handlers

    def set_dispatcher_handlers(self) -> None:
        for handler_group in self.handlers:
            for handler in handler_group.handlers:
                self.updater.dispatcher.add_handler(handler, group=handler_group.group_index)

    def set_commands(self) -> None:
        self.updater.bot.set_my_commands(self.commands)

    def run(self) -> None:
        self.updater.start_polling()
        self.updater.idle()

    def initialize(self) -> None:
        self.set_dispatcher_handlers()
        self.set_commands()


class COTDBotService:
    def __init__(self, client: TGBotClient, config: COTDBotConfig):
        self.client = client
        self.logger = config.logger
        self.features = config.features

    def get_stickers(self) -> COTDBotStickers:
        fileids = []

        if not (sticker_pack := self._fetch_sticker_set()):
            self._init_sticker_set()
            sticker_pack = self._fetch_sticker_set()

        return COTDBotStickers(
            **{
                "sticker_set": sticker_pack,
                "sticker_set_file_ids": fileids.extend(
                    list(sticker.file_id for sticker in sticker_pack.stickers)
                ),
            }
        )

    def _init_sticker_set(self) -> bool:
        assert self.client.metadata.user is not None

        return self.client.updater.bot.create_new_sticker_set(
            png_sticker=open("static/smileyOne512x512.png", "rb"),
            name=f"VC_by_{self.client.metadata.user.username}",
            title=f"VC_by_{self.client.metadata.user.username}",
            user_id=int(145043750),
            emojis="🙂😊",
        )

    def _fetch_sticker_set(self) -> telegram.StickerSet:
        assert self.client.metadata.user is not None

        try:
            return self.client.updater.bot.get_sticker_set(
                f"VC_by_{self.client.metadata.user.username}"
            )
        except telegram.error.BadRequest as err:
            raise err

    @property
    def stickers(self):
        return self.get_stickers()


def factory(
    envs: EnvConfig,
    features: Flags,
    options: Options,
    client_logger: logging.Logger,
    cotd_logger: logging.Logger,
    commands: typing.List[telegram.BotCommand],
    handlers: typing.List[HandlerGroup],
    storage: cotd.storage.TelegramSavedMessagesStorage,
) -> COTDBotService:

    if features.enable_persistence:
        updater = telegram.ext.Updater(
            token=envs.token,
            use_context=True,
            persistence=storage,
            defaults=telegram.ext.Defaults(
                parse_mode="HTML",
                disable_notification=True,
                disable_web_page_preview=True,
                timeout=5.0,
            ),
        )
    else:
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

    updater.logger = client_logger
    updater.dispatcher.logger = client_logger

    metadata = TGBotMetadata(updater.bot.get_me())

    tg_bot_client = TGBotClient(
        TGBotConfig(
            updater=updater,
            options=options,
            metadata=metadata,
            handlers=handlers,
            commands=commands,
        )
    )
    return COTDBotService(
        tg_bot_client, config=COTDBotConfig(features=features, logger=cotd_logger)
    )
