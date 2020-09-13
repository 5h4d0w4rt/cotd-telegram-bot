import argparse


def define_feature_flags(parser: argparse.ArgumentParser):
    parser.add_argument('--incomplete-feature-x')


def parse_feature_flags(parser: argparse.ArgumentParser, args):
    define_feature_flags(parser)
    return parser.parse_args(args)
