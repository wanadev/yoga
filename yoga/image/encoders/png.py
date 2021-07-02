import io
import zlib
import struct

import zopfli


_PNG_MAGIC = b"\x89PNG\r\n\x1A\n"
_PNG_COLOR_TYPES = {
    0: "grayscale",
    2: "truecolour",
    3: "indexed-colour",
    4: "grayscale-alpha",
    6: "truecolour-alpha",
}
_PNG_COMPRESSION_METHODS = {
    0: "deflate",
}
_PNG_FILTER_METHODS = {
    0: "adaptative",
}
_PNG_INTERLACE_METHODS = {
    0: "no-interlace",
    1: "Adam7",
}


def big_endian_uint32_bytes_to_python_int(bytes_):
    return struct.unpack(">L", bytes_)[0]


def python_int_to_big_endian_uint32_bytes(number):
    return struct.pack(">L", number)


def get_png_structure(data):
    if not is_png(data):
        raise ValueError("Unvalid PNG: Not a PNG file")

    result = {
        "size": len(data),
        "chunks": [],
    }

    offset = len(_PNG_MAGIC)

    while offset < result["size"]:
        chunk = {
            "type": data[offset + 4 : offset + 8].decode(),
            "data_offset": offset + 8,
            "size": big_endian_uint32_bytes_to_python_int(
                data[offset : offset + 4]
            ),
            "crc": None,
        }
        chunk["crc"] = big_endian_uint32_bytes_to_python_int(
            data[
                chunk["data_offset"]
                + chunk["size"] : chunk["data_offset"]
                + chunk["size"]
                + 4
            ]
        )
        result["chunks"].append(chunk)
        offset += 12 + chunk["size"]

    return result


def get_IHDR_info(data):
    return {
        "width": big_endian_uint32_bytes_to_python_int(data[0:4]),
        "height": big_endian_uint32_bytes_to_python_int(data[4:8]),
        "bit_depth": data[8],
        "colour_type": data[9],
        "colour_type_str": _PNG_COLOR_TYPES[data[9]],
        "compression_method": data[10],
        "compression_method_str": _PNG_COMPRESSION_METHODS[data[10]],
        "filter_method": data[11],
        "filter_method_str": _PNG_FILTER_METHODS[data[11]],
        "interlace_method": data[12],
        "interlace_method_str": _PNG_INTERLACE_METHODS[data[12]],
    }


def assemble_png_from_chunks(chunks):
    """Assemble a PNG file from a list of chunks

    :param list chunks: The list of chunks (see bellow).

    Example list of chunk::

        [
            {
                "type": "IHDR",
                "data": b"...",
            },
            {
                "type": "PLTE",
                "data": b"...",
            },
            {
                "type": "IDAT",
                "data": b"...",
            },
            {
                "type": "IEND",
                "data": b"",
            },
        ]

    .. WARNING::

        All chunks should be provided in the right order. The first chunk
        should be ``IHDR`` and the last one ``IEND``.

    :rtype: bytes
    """
    result_png = _PNG_MAGIC

    for chunk in chunks:
        result_png += python_int_to_big_endian_uint32_bytes(len(chunk["data"]))
        result_png += bytes(chunk["type"], encoding="ascii")
        result_png += chunk["data"]
        result_png += python_int_to_big_endian_uint32_bytes(
            zlib.crc32(
                chunk["data"],
                zlib.crc32(bytes(chunk["type"], encoding="ascii")),
            )
        )

    return result_png


def clean_png(data):
    """Cleans the given PNG.

    * Removes non-essential chunks,
    * Concat all the ``IDAT`` chunks,
    * Recompress the ``IDAT`` chunk with Zopfli or keep the original
      compression if more efficient.

    :param bytes data: the raw PNG data.
    :rtype: bytes
    """
    png_structure = get_png_structure(data)
    chunks = []
    idat_concat = b""

    # Keep essential chunks and concat IDAT chunks
    for chunk in png_structure["chunks"]:
        if chunk["type"] in ["IHDR", "PLTE", "tRNS"]:
            chunks.append(
                {
                    "type": chunk["type"],
                    "data": data[
                        chunk["data_offset"] : chunk["data_offset"]
                        + chunk["size"]
                    ],
                }
            )
        elif chunk["type"] == "IDAT":
            idat_concat += data[
                chunk["data_offset"] : chunk["data_offset"] + chunk["size"]
            ]

    # Recompress IDAT chunk with Zopfli
    compressor = zopfli.ZopfliCompressor(
        format=zopfli.ZOPFLI_FORMAT_ZLIB,
        iterations=150,
    )
    idat_zopfli = (
        compressor.compress(zlib.decompress(idat_concat)) + compressor.flush()
    )

    # Add the IDAT chunk
    chunks.append(
        {
            "type": "IDAT",
            "data": idat_zopfli
            if len(idat_zopfli) <= len(idat_concat)
            else idat_concat,
        }
    )

    # ... and the IEND one to finish the file :)
    chunks.append(
        {
            "type": "IEND",
            "data": b"",
        }
    )

    return assemble_png_from_chunks(chunks)


def is_png(file_bytes):
    """Whether or not the given bytes represent a PNG file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a PNG file, ``False`` else.
    """
    return file_bytes.startswith(_PNG_MAGIC)


def optimize_png(image, raw_data, slow=False):
    """Encode image to PNG using ZopfliPNG.

    :param PIL.Image image: The image to encode.
    :param bytes raw_data: Raw input data.
    :param bool slow: Makes a little bit more efficient optimization (in some
                      cases) but runs very slow.

    :returns: The encoded image's bytes.
    """
    image_io = io.BytesIO()
    image.save(image_io, format="PNG", optimize=False)
    image_io.seek(0)
    image_bytes = image_io.read()

    # Optimize using ZopfliPNG
    zopflipng = zopfli.ZopfliPNG()
    zopflipng.lossy_8bit = True
    zopflipng.lossy_transparent = True

    if slow:
        zopflipng.filter_strategies = "01234mepb"
        zopflipng.iterations = 20
        zopflipng.iterations_large = 7

    zopfli_bytes = zopflipng.optimize(image_bytes)

    # Try to fix the output if it is larger than the input
    if is_png(raw_data) and len(zopfli_bytes) > len(raw_data):
        png_structure = get_png_structure(raw_data)
        ihdr_chunk = png_structure["chunks"][0]
        png_header = get_IHDR_info(
            raw_data[
                ihdr_chunk["data_offset"] : ihdr_chunk["data_offset"]
                + ihdr_chunk["size"]
            ]
        )

        # Only use data from input image if it has not been resized
        if (
            image.width == png_header["width"]
            and image.height == png_header["height"]
        ):
            return clean_png(raw_data)

    return zopfli_bytes
