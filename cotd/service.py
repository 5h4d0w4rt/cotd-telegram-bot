import telegram
import telegram.ext
import logging
import argparse
import typing
from dataclasses import dataclass


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
class Config:
    env: EnvConfig
    updater: telegram.ext.Updater
    logger: logging.Logger
    options: argparse.Namespace
    metadata: TGBotMetadata
    handlers: typing.List[telegram.ext.Handler]
    commands: typing.List[telegram.BotCommand]


@dataclass
class COTDBotConfig(Config):
    features: argparse.Namespace


class TGBotClient:

    def __init__(self, config: Config):
        self.env = config.env
        self.options = config.options
        self.logger = config.logger
        self.updater = config.updater
        self.metadata = config.metadata
        self.commands = config.commands
        self.handlers = config.handlers

    def set_dispatcher_handlers(self) -> None:
        for handler in self.handlers:
            self.updater.dispatcher.add_handler(handler)

    def set_commands(self) -> None:
        self.updater.bot.set_my_commands(self.commands)

    def run(self) -> None:
        self.updater.start_polling()
        self.updater.idle()

    def initialize(self) -> None:
        self.set_dispatcher_handlers()
        self.set_commands()


class COTDBotService(TGBotClient):

    def __init__(self, config: COTDBotConfig):
        super().__init__(config)
        self.features = config.features

    def get_stickers(self) -> COTDBotStickers:
        fileids = []

        if not (sticker_pack := self._fetch_sticker_set()):
            sticker_pack = self._init_sticker_set()

        return COTDBotStickers(**{
            'sticker_set': sticker_pack, 'sticker_set_file_ids': fileids.extend(
                list(sticker.file_id for sticker in sticker_pack.stickers)
            )
        })

    def _init_sticker_set(self) -> telegram.StickerSet:
        return self.updater.bot.create_new_sticker_set(
            png_sticker=open("static/smileyOne512x512.png", 'rb'),
            name=f"VC_by_{self.metadata.user.username}",
            title=f"VC_by_{self.metadata.user.username}",
            user_id=int(145043750),
            emojis="🙂😊")

    def _fetch_sticker_set(self) -> typing.Union[telegram.StickerSet, bool, None]:
        try:
            return self.updater.bot.get_sticker_set(f"VC_by_{self.metadata.user.username}")
        except telegram.error.BadRequest as err:
            if 'Stickerset_invalid' in str(err):
                return False
            else:
                raise

    @property
    def stickers(self):
        return self.get_stickers()
