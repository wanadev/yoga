import os
import argparse
from functools import partial

from .image.cli import add_image_cli_options
from .model.cli import add_model_cli_options
from .version import VERSION


def _type_path(mode, string):
    if os.path.isfile(string):
        if os.access(string, mode):
            return string
        raise argparse.ArgumentTypeError("can't access '%s'" % string)
    else:
        path = os.path.dirname(os.path.abspath(string))
        if os.access(path, mode):
            return string
        raise argparse.ArgumentTypeError(
            "the '%s' folder does not exist" % path
        )


def add_main_cli_arguments(parser):
    parser.add_argument(
        "input",
        help="Input file path",
        type=partial(_type_path, os.R_OK),
    )
    parser.add_argument(
        "output",
        help="Output file path",
        type=partial(_type_path, os.W_OK),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="enable verbose mode",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="enable quiet mode (takes precedence over verbose)",
        default=False,
        action="store_true",
    )


def generate_image_cli(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()
    add_main_cli_arguments(parser)
    add_image_cli_options(parser)
    return parser


def generate_model_cli(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()
    add_main_cli_arguments(parser)
    model_group = parser.add_argument_group(title="model options")
    add_model_cli_options(model_group)
    image_group = parser.add_argument_group(title="image options")
    add_image_cli_options(image_group, prefix="image-")
    return parser


def generate_main_cli():
    parser = argparse.ArgumentParser(
        prog="yoga",
        usage="%(prog)s [-h] {image,model} [options...] input output",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%%(prog)s %s" % VERSION,
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    image_parser = subparsers.add_parser(
        "image",
        prog="yoga image",
        help="Converts and optimizes images",
    )
    generate_image_cli(image_parser)

    model_parser = subparsers.add_parser(
        "model",
        prog="yoga model",
        help="Converts and optimizes 3D models",
    )
    generate_model_cli(model_parser)

    return parser
