from .encoders.jpeg import is_jpeg
from .encoders.png import is_png
from .encoders.webp import is_lossy_webp
from .encoders.webp_lossless import is_lossless_webp


def image_have_alpha(image, threshold=0xFE):
    if threshold <= 0:
        return False
    # TODO find transparent colors in indexed images (image.mode == "P")
    if image.mode != "RGBA":
        return False
    alpha_band = image.getdata(band=3)  # bands: R=0, G=1, B=2, A=3
    for pix in alpha_band:
        if pix <= threshold:
            return True
    return False


def guess_image_format(image_bytes):
    FORMATS = {
        "jpeg": is_jpeg,
        "png": is_png,
        "webp": is_lossy_webp,
        "webpl": is_lossless_webp,
    }

    for format_, checker in FORMATS.items():
        if checker(image_bytes):
            return format_

    raise ValueError("Unsupported image format")
