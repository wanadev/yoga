import io

from .webp import is_riff
from .webp import get_riff_structure


def is_lossless_webp(file_bytes):
    """Whether or not the given bytes represent a lossless WEBP file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a lossless WEBP file, ``False``
             else.
    """
    if not is_riff(file_bytes):
        return False

    riff = get_riff_structure(file_bytes)

    if riff["formtype"] == "WEBP":
        chunks = [chunk["type"] for chunk in riff["chunks"]]
        if "VP8L" in chunks:
            return True

    return False


def optimize_lossless_webp(image):
    """Encode image to lossless WEBP using Pillow.

    :param PIL.Image image: The image to encode.

    :returns: The encoded image's bytes.
    """
    image_io = io.BytesIO()
    image.save(
        image_io,
        format="WEBP",
        lossless=True,
        quality=100,
        method=6,
    )
    image_io.seek(0)
    return image_io.read()
