#!/usr/bin/env python

import sys

from PIL import Image
from PIL.ExifTags import TAGS


def print_exif(input_path):
    image = Image.open(input_path)
    exif = image.getexif()

    print("+-- %s" % input_path)
    for key, value in exif.items():
        print("    +-- [%i] %s: %s" % (key, TAGS[key], value))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE:")
        print(
            "  ./scripts/lsexif.py <image.jpg> [image2.jpg ...]"
        )
        sys.exit(1)

    for input_path in sys.argv[1:]:
        print_exif(input_path)
