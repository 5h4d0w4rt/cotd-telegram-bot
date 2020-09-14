import telegram.ext
import logging
import argparse


class EnvConfig:

    def __init__(self, token):
        self.token = token


class Config:

    def __init__(self,
                 env: EnvConfig = None,
                 features: argparse.Namespace = None,
                 options: argparse.Namespace = None,
                 logger: logging.Logger = None):
        self.env = env
        self.features = features
        self.options = options
        self.logger = logger


class COTDBot:

    def __init__(self, config: Config):
        self.config = config
        self.updater = self._updater()

    def _updater(self):
        return telegram.ext.Updater(
            token=self.config.env.token,
            use_context=True,
            defaults=telegram.ext.Defaults(
                parse_mode='HTML',
                disable_notification=True,
                disable_web_page_preview=True,
                timeout=5.0,
            ))
