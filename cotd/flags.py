import argparse


def define_feature_flags(parser: argparse.ArgumentParser):
    pass


def parse_feature_flags(parser: argparse.ArgumentParser, args):
    define_feature_flags(parser)
    return parser.parse_known_args(args)[0]
