import argparse

from .image.cli import add_image_cli_options
from .model.cli import add_model_cli_options


def add_main_cli_arguments(parser):
    parser.add_argument(
            "input",
            help="Input file path",
            type=argparse.FileType("rb")
            )
    parser.add_argument(
            "output",
            help="Output file path",
            type=argparse.FileType("wb")
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
    parser = argparse.ArgumentParser(prog="yoga")
    subparsers = parser.add_subparsers(dest="subcommand")

    image_parser = subparsers.add_parser(
            "image",
            help="Converts and optimizes images"
            )
    generate_image_cli(image_parser)

    model_parser = subparsers.add_parser(
            "model",
            help="Converts and optimizes 3D models"
            )
    generate_model_cli(model_parser)

    return parser
