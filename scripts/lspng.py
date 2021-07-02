#!/usr/bin/env python

import sys
import struct
import zlib

from yoga.image.encoders import png


def big_endian_uint16_bytes_to_python_int(bytes_):
    return struct.unpack(">H", bytes_)[0]


def get_sBIT_info(data, colour_type):
    if colour_type == 0:  # Grayscale
        return {
            "significant_greyscale_bits": data[0],
        }
    elif colour_type in [2, 3]:  # Truecolour, Indexed-colour
        return {
            "significant_red_bits": data[0],
            "significant_green_bits": data[1],
            "significant_blue_bits": data[2],
        }
    elif colour_type == 4:  # Grayscale with alpha
        return {
            "significant_greyscale_bits": data[0],
            "significant_alpha_bits": data[1],
        }
    elif colour_type == 6:  # Truecolour with alpha
        return {
            "significant_red_bits": data[0],
            "significant_green_bits": data[1],
            "significant_blue_bits": data[2],
            "significant_alpha_bits": data[3],
        }


def get_pHYs_info(data):
    PNG_UNITS = {
        0: "unknown",
        1: "metre",
    }
    return {
        "pixels_per_unit_x": png.big_endian_uint32_bytes_to_python_int(
            data[0:4]
        ),
        "pixels_per_unit_y": png.big_endian_uint32_bytes_to_python_int(
            data[4:8]
        ),
        "unit_specifier": data[8],
        "unit_specifier_str": PNG_UNITS[data[8]],
    }


def get_tEXt_info(data):
    for i in range(len(data)):
        if data[i] == 0:
            return {
                data[0:i].decode(): data[i + 1 :].decode(),
            }


def get_tIME_info(data):
    return {
        "year": big_endian_uint16_bytes_to_python_int(data[:2]),
        "month": data[2],
        "day": data[3],
        "hour": data[4],
        "minute": data[5],
        "second": data[6],
    }


def get_bKGD_info(data, colour_type):
    if colour_type in [0, 4]:  # Grayscale, Grayscale with alpha
        return {"grayscale": big_endian_uint16_bytes_to_python_int(data)}
    elif colour_type in [2, 6]:  # Truecolour, Truecolour with alpha
        return {
            "red": big_endian_uint16_bytes_to_python_int(data[0:2]),
            "green": big_endian_uint16_bytes_to_python_int(data[2:4]),
            "blue": big_endian_uint16_bytes_to_python_int(data[4:6]),
        }
    elif colour_type == 3:  # Indexed-colour
        return {
            "palette_index": data[0],
        }


def calculate_crc32(image_data, chunk_info):
    return zlib.crc32(
        image_data[
            chunk_info["data_offset"]
            - 4 : chunk_info["data_offset"]
            + chunk_info["size"]
        ]
    )


def print_png_info(input_path):
    image = open(input_path, "rb").read()
    png_structure = png.get_png_structure(image)

    print("+-- %s" % input_path)
    print("    +-- PNG [size: %i]" % png_structure["size"])

    for chunk in png_structure["chunks"]:
        print(
            "        +-- %s [offset: %i, size: %i, crc: %08X (%s)]"
            % (
                chunk["type"],
                chunk["data_offset"],
                chunk["size"],
                chunk["crc"],
                "ok"
                if calculate_crc32(image, chunk) == chunk["crc"]
                else "error",
            )
        )
        if chunk["type"] == "IHDR":
            ihdr_info = png.get_IHDR_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ]
            )
            for key, value in ihdr_info.items():
                print("            +-- %s: %s" % (key, str(value)))
        elif chunk["type"] == "sBIT":
            info = get_sBIT_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ],
                ihdr_info["colour_type"],
            )
            for key, value in info.items():
                print("            +-- %s: %s" % (key, str(value)))
        elif chunk["type"] == "pHYs":
            info = get_pHYs_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ]
            )
            for key, value in info.items():
                print("            +-- %s: %s" % (key, str(value)))
        elif chunk["type"] == "tEXt":
            info = get_tEXt_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ]
            )
            for key, value in info.items():
                print("            +-- %s: %s" % (key, str(value)))
        elif chunk["type"] == "tIME":
            info = get_tIME_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ]
            )
            for key, value in info.items():
                print("            +-- %s: %s" % (key, str(value)))
        elif chunk["type"] == "bKGD":
            info = get_bKGD_info(
                image[
                    chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
                ],
                ihdr_info["colour_type"],
            )
            for key, value in info.items():
                print("            +-- %s: %s" % (key, str(value)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE:")
        print("  ./scripts/lspng.py <image.png> [image2.png ...]")
        sys.exit(1)

    for input_path in sys.argv[1:]:
        print_png_info(input_path)
