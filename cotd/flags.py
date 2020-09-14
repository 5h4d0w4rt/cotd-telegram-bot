import argparse


def define_feature_flags(parser: argparse.ArgumentParser):
    parser.add_argument('--incomplete-create-sticker-set', action="store_true", default=False)


def parse_feature_flags(parser: argparse.ArgumentParser, args):
    define_feature_flags(parser)
    return parser.parse_known_args(args)
