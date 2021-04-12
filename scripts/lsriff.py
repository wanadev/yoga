#!/usr/bin/env python

import sys

from yoga.image.encoders.webp import get_riff_structure


def print_riff_info(input_path):
    image = open(input_path, "rb").read()
    riff = get_riff_structure(image)

    print("+-- %s" % input_path)
    print(
        "    +-- RIFF [size: %i, formtype: %s]"
        % (riff["size"], riff["formtype"])
    )

    for chunk in riff["chunks"]:
        print(
            "        +-- %s [offset: %i, size: %i]"
            % (chunk["type"], chunk["data_offset"], chunk["size"])
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE:")
        print(
            "  ./scripts/lsriff.py <image.webp> [image2.webp [image3.webp [...]]]"
        )
        sys.exit(1)

    for input_path in sys.argv[1:]:
        print_riff_info(input_path)
