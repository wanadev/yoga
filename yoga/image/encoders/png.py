import io

import zopfli


def is_png(file_bytes):
    """Whether or not the given bytes represent a PNG file.

    :params bytes file_bytes: The bytes of the file to check.

    :rtype: bool
    :return: ``True`` if the bytes represent a PNG file, ``False`` else.
    """
    return file_bytes.startswith(b"\x89PNG\r\n")


def optimize_png(image, slow=False):
    """Encode image to PNG using ZopfliPNG.

    :param PIL.Image image: The image to encode.
    :param bool slow: Makes a little bit more efficient optimization (in some
                      cases) but runs very slow.

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

    if slow:
        zopflipng.filter_strategies = "01234mepb"
        zopflipng.iterations = 20
        zopflipng.iterations_large = 7

    return zopflipng.optimize(image_bytes)
