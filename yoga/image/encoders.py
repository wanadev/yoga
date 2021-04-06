import io

import pyguetzli
import zopfli


def jpeg(image, quality):
    """Encode image to JPEG using Guetzli.

    :param PIL.Image image: The image to encode.
    :param float quality: The output JPEG quality (from ``0.00``to ``1.00``).

    :returns: The encoded image's bytes.
    """
    if not 0.00 <= quality <= 1.00:
        raise ValueError("JPEG quality value must be between 0.00 and 1.00")
    return pyguetzli.process_pil_image(image, int(quality * 100))


def png(image):
    """Encode image to PNG using ZopfliPNG.

    :param PIL.Image image: The image to encode.

    :returns: The encoded image's bytes.
    """
    # Export the image as a PNG file-like bytes
    image_io = io.BytesIO()
    image.save(image_io, format="PNG", optimize=False)
    image_io.seek(0)
    image_bytes = image_io.read()

    # Optimize using ZopfliPNG
    zopflipng = zopfli.ZopfliPNG()
    zopflipng.lossy_8bit = True
    zopflipng.lossy_transparent = True
    zopflipng.filter_strategies = "01234mepb"
    zopflipng.iterations = 20
    zopflipng.iterations_large = 7

    return zopflipng.optimize(image_bytes)
