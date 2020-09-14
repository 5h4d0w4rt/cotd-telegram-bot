import telegram.ext


class EnvConfig:

    def __init__(self, token):
        self.token = token


class FeatureFlagsConfig:

    def __init__(self, features):
        self.features = features


class OptionsConfig:

    def __init__(self, options):
        self.options = options


class ClientsConfig:

    def __init__(self, telegram_bot_updater_client: telegram.ext.Updater):
        self.telegram_bot_updater_client = telegram_bot_updater_client


class Config:

    def __init__(self, env: EnvConfig, features: FeatureFlagsConfig,
                 options: OptionsConfig, logger):
        self.env = env
        self.features = features
        self.options = options
        self.logger = logger


class COTDBot:

    def __init__(self, config: Config):
        self.config = config
        self.updater = self._updater()

    def _updater(self):
        return telegram.ext.Updater(token=self.config.env.token,
                                    use_context=True,
                                    defaults=telegram.ext.Defaults(
                                        parse_mode='HTML',
                                        disable_notification=True,
                                        disable_web_page_preview=True,
                                        timeout=5.0,
                                    ))
