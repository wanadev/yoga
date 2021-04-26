import argparse
from functools import partial

from .options import DEFAULT_OPTIONS, _RESIZE_OPTION_REGEXP


def _type_resize(string):
    string = string.lower()
    if string == "orig":
        return string
    if string.isdigit():
        return string
    if _RESIZE_OPTION_REGEXP.match(string):
        return string
    message = (
        "invalid format: '%s' (valid formats are "
        "'orig', <SIZE>, <WIDTH>x<HEIGHT>)"
    ) % string
    raise argparse.ArgumentTypeError(message)


def _type_range(min_, max_, string):
    value = 0
    try:
        value = float(string)
    except ValueError:
        message = "invalid number: '%s'" % string
        raise argparse.ArgumentTypeError(message)
    if min_ <= value <= max_:
        return value
    message = "number not in range: '%s' (range is [%i-%i])" % (
        string,
        min_,
        max_,
    )
    raise argparse.ArgumentTypeError(message)


def add_image_cli_options(parser, prefix=""):
    parser.add_argument(
        "--%soutput-format" % prefix,
        help="format of the output image",
        metavar="{orig,auto,jpeg,png,webp,webpl}",
        choices=["orig", "auto", "jpeg", "jpg", "png", "webp", "webpl"],
        default=DEFAULT_OPTIONS["output_format"],
    )
    parser.add_argument(
        "--%sresize" % prefix,
        help="resize the image",
        metavar="{orig,<SIZE>,<WIDTH>x<HEIGHT>}",
        type=_type_resize,
        default=DEFAULT_OPTIONS["resize"],
    )
    parser.add_argument(
        "--%sjpeg-quality" % prefix,
        help="JPEG quality if the output format is set to 'jpeg'",
        metavar="0-100",
        type=partial(_type_range, 0, 100),
        default=DEFAULT_OPTIONS["jpeg_quality"],
    )
    parser.add_argument(
        "--%swebp-quality" % prefix,
        help="WEBP quality if the output format is set to 'webp'",
        metavar="0-100",
        type=partial(_type_range, 0, 100),
        default=DEFAULT_OPTIONS["webp_quality"],
    )
    parser.add_argument(
        "--%sopacity-threshold" % prefix,
        help="threshold below which a pixel is considered transparent",
        metavar="0-255",
        type=partial(_type_range, 0, 255),
        default=DEFAULT_OPTIONS["opacity_threshold"],
    )
    parser.add_argument(
        "--%spng-slow-optimization" % prefix,
        help="enable a (very) slow optimization preset for PNGs that can sometimes gain few bytes on the output file",
        action="store_true",
    )
