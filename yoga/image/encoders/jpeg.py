import pyguetzli
import mozjpeg_lossless_optimization
from PIL import Image


EXIF_TAG_ORIENTATION = 0x0112
ORIENTATION_OPERATIONS = {
    1: [],
    2: [Image.FLIP_LEFT_RIGHT],
    3: [Image.ROTATE_180],
    4: [Image.FLIP_TOP_BOTTOM],
    5: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
    6: [Image.ROTATE_270],
    7: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
    8: [Image.ROTATE_90],
}


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
    guetzli_jpeg_bytes = pyguetzli.process_pil_image(image, int(quality * 100))
    return mozjpeg_lossless_optimization.optimize(guetzli_jpeg_bytes)


def open_jpeg(image_file):
    """Open JPEG file.

    This function also handles JPEG Orientation EXIF.

    :param file-like image_file: the image file.
    :rtype: PIL.Image
    """
    image = Image.open(image_file)
    exif = image.getexif()

    if (
        EXIF_TAG_ORIENTATION in exif
        and exif[EXIF_TAG_ORIENTATION] in ORIENTATION_OPERATIONS
    ):
        orientation = exif[EXIF_TAG_ORIENTATION]
        for operation in ORIENTATION_OPERATIONS[orientation]:
            image = image.transpose(operation)

    return image
