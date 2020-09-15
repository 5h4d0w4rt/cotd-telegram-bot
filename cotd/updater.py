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
class Config:
    env: EnvConfig
    updater: telegram.ext.Updater
    logger: logging.Logger
    options: argparse.Namespace


@dataclass
class COTDBotConfig(Config):
    features: argparse.Namespace


@dataclass
class TGBotMetadata:
    user: telegram.User


@dataclass
class COTDBotMetadata(TGBotMetadata):
    sticker_set: telegram.StickerSet
    sticker_set_file_ids: typing.List[str]


class TGBotClient:

    def __init__(self, config: Config):
        self.env = config.env
        self.options = config.options
        self.logger = config.logger
        self.updater = config.updater
        self.metadata = TGBotMetadata(user=self.__fetch_user_metadata(self.updater))

        self.__init_loggers(
            base_logger=self.logger,
            updater_logger=self.updater.logger,
            dispatcher_logger=self.updater.dispatcher.logger)

    def __fetch_user_metadata(self, updater: telegram.ext.Updater) -> telegram.User:
        return updater.bot.get_me()

    def __init_loggers(self, base_logger: logging.Logger, dispatcher_logger: logging.Logger,
                       updater_logger: logging.Logger) -> None:
        base_logger.setLevel(self.options.log_level)

        updater_logger.setLevel(self.options.log_level)
        updater_logger.addHandler(logging.StreamHandler())

        dispatcher_logger.setLevel(self.options.log_level)
        dispatcher_logger.addHandler(logging.StreamHandler())


class COTDBot(TGBotClient):

    def __init__(self, config: COTDBotConfig):
        TGBotClient.__init__(self, config)
        self.features = config.features
        self.metadata = self.fetch_metadata(self.updater, self.metadata.user)

    def fetch_metadata(self, updater: telegram.ext.Updater, me: telegram.User) -> COTDBotMetadata:

        if not (sticker_pack := self._fetch_sticker_set(updater, me)):
            sticker_pack = self._init_sticker_set(updater, me)

        fileids = []

        return COTDBotMetadata(**{
            'user': me,
            'sticker_set': sticker_pack, 'sticker_set_file_ids': fileids.extend(
                list(sticker.file_id for sticker in sticker_pack.stickers)
            )
        })

    def _init_sticker_set(self, updater: telegram.ext.Updater, me: telegram.User):
        return updater.bot.create_new_sticker_set(
            png_sticker=open("static/smileyOne512x512.png", 'rb'),
            name=f"VC_by_{me.username}",
            title=f"VC_by_{me.username}",
            user_id=int(145043750),
            emojis="🙂😊")

    def _fetch_sticker_set(
        self, updater: telegram.ext.Updater, me: telegram.User
                           ) -> typing.Tuple[telegram.StickerSet, typing.List[str]]:
        try:
            return updater.bot.get_sticker_set(f"VC_by_{me.username}")
        except telegram.error.BadRequest as err:
            if 'Stickerset_invalid' in str(err):
                return False
            else:
                raise
