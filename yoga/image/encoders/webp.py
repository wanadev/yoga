import io
import struct


def little_endian_unint32_bytes_to_python_int(bytes_):
    return struct.unpack("<L", bytes_)[0]


def get_riff_structure(data):
    if data[0:4] != b"RIFF":
        raise ValueError("Unvalid RIFF: Not a RIFF file")

    result = {
        "formtype": data[8:12].decode(),
        "size": little_endian_unint32_bytes_to_python_int(data[4:8]),
        "chunks": [],
    }

    if result["size"] + 8 != len(data):
        raise ValueError("Unvalid RIFF: Truncated data")

    offset = 12  # RIFF header length

    while offset < len(data):
        chunk = {
            "type": data[offset : offset + 4].decode(),
            "data_offset": offset + 8,
            "size": little_endian_unint32_bytes_to_python_int(
                data[offset + 4 : offset + 8]
            ),
        }
        result["chunks"].append(chunk)
        offset += 8 + chunk["size"] + chunk["size"] % 2

    return result


def get_vp8x_info(data):
    # fmt: off
    #                   RRILEXAR
    VP8X_FLAG_ICC   = 0b00100000  # noqa: E221
    VP8X_FLAG_ALPHA = 0b00010000  # noqa: E221
    VP8X_FLAG_EXIF  = 0b00001000  # noqa: E221
    VP8X_FLAG_XMP   = 0b00000100  # noqa: E221
    VP8X_FLAG_ANIM  = 0b00000010  # noqa: E221
    # fmt: on

    if len(data) != 10:
        ValueError("Invaild VP8X data")

    return {
        "has_icc": bool(data[0] & VP8X_FLAG_ICC),
        "has_alpha": bool(data[0] & VP8X_FLAG_ALPHA),
        "has_exif": bool(data[0] & VP8X_FLAG_EXIF),
        "has_xmp": bool(data[0] & VP8X_FLAG_XMP),
        "has_anim": bool(data[0] & VP8X_FLAG_ANIM),
        "canvas_width": little_endian_unint32_bytes_to_python_int(
            data[4:7] + b"\x00"
        )
        + 1,
        "canvas_height": little_endian_unint32_bytes_to_python_int(
            data[7:10] + b"\x00"
        )
        + 1,
    }


def is_riff(file_bytes):
    """Whether or not the given bytes represent a RIFF file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a RIFF file, ``False`` else.
    """
    return file_bytes.startswith(b"RIFF")


def is_lossy_webp(file_bytes):
    """Whether or not the given bytes represent a lossy WEBP file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a lossy WEBP file, ``False`` else.
    """
    if not is_riff(file_bytes):
        return False

    riff = get_riff_structure(file_bytes)

    if riff["formtype"] == "WEBP":
        chunks = [chunk["type"] for chunk in riff["chunks"]]
        if "VP8 " in chunks:
            return True

    return False


def optimize_lossy_webp(image, quality):
    """Encode image to lossy WEBP using Pillow.

    :param PIL.Image image: The image to encode.
    :param float quality: The output WEBP quality (from ``0.00``to ``1.00``).

    :returns: The encoded image's bytes.
    """
    if not 0.00 <= quality <= 1.00:
        raise ValueError("WEBP quality value must be between 0.00 and 1.00")

    image_io = io.BytesIO()
    image.save(
        image_io,
        format="WEBP",
        lossless=False,
        quality=int(quality * 100),
        method=6,
    )
    image_io.seek(0)
    return image_io.read()
