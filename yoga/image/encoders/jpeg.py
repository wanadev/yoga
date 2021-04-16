import pyguetzli


def is_jpeg(file_bytes):
    """Whether or not the given bytes represent a JPEG file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a JPEG file, ``False`` else.
    """
    JPEG_MAGICS = [
        b"\xFF\xD8\xFF\xDB",
        b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01",  # JFIF format
        b"\xFF\xD8\xFF\xEE",
        b"\xFF\xD8\xFF\xE1",  # xx xx 45 78 69 66 00 00  / Exif format
    ]
    for magic in JPEG_MAGICS:
        if file_bytes.startswith(magic):
            return True
    return False


def optimize_jpeg(image, quality):
    """Encode image to JPEG using Guetzli.

    :param PIL.Image image: The image to encode.
    :param float quality: The output JPEG quality (from ``0.00``to ``1.00``).

    :returns: The encoded image's bytes.
    """
    if not 0.00 <= quality <= 1.00:
        raise ValueError("JPEG quality value must be between 0.00 and 1.00")
    return pyguetzli.process_pil_image(image, int(quality * 100))
