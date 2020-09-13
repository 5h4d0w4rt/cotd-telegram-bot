import argparse


class Config:

    def __init__(self, env, features, options):
        self.env = env
        self.features = features
        self.options = options


class EnvConfig:

    def __init__(self, token):
        self.token = token


class FeatureFlagsConfig:

    def __init__(self, features):
        self.features = features


class OptionsConfig:

    def __init__(self, options):
        self.options = options