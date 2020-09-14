import argparse


def define_options(parser: argparse.ArgumentParser):
    parser.add_argument('--mode', choices=["token", "webhook"])


def parse_options(parser: argparse.ArgumentParser, args):
    define_options(parser)
    return parser.parse_known_args(args)
