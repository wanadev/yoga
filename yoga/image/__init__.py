"""
This module allows to convert and optimize images.

Usage
-----

Converting and optimizing an image::

    import yoga.image
    yoga.image.optimize("./input.png", "./output.png")

You can also tune the output by passing options::

    yoga.image.optimize("./input.png", "./output.png", options={
        "output_format": "orig",   # "orig"|"auto"|"jpeg"|"png"
        "resize": "orig",          # "orig"|[width,height]
        "jpeg_quality": 0.84,      # 0.00-1.0
        "opacity_threshold": 254,  # 0-255
    })


.. _yoga_image_api_options:

Available Options
-----------------

output_format
~~~~~~~~~~~~~

The format of the output image.

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "output_format": "orig",
    })

The following formats are supported:

* ``orig``: This is the default. The output format will be the same as the one
  of the input image.
* ``auto``: The output format is automatically selected. YOGA will generate a
  PNG if the input image is using transparency, else it will generate a JPEG.
* ``png``: Outputs a PNG image.
* ``jpeg``: Outputs a JPEG image.

.. NOTE::

   When using the ``"orig"`` output format, YOGA will only accept PNGs and
   JPEGs images as input.


resize
~~~~~~

Resize the output image.

Allowed values are:

* ``"orig"``: The default. Keeps the original size (no resize).
* ``[width, height]``: The box in which the image should fit.

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "resize": "orig",
    })

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "resize": [512, 512],
    })

.. NOTE::

   YOGA always preserve the image's aspect ratio; you can consider the size you
   provide as a box the image will fit in.


jpeg_quality
~~~~~~~~~~~~

The quality of the output JPEGs.

The value is a number between ``0.00`` and ``1.00`` (``0.84`` by default):

* ``0.00``: ugly images but smaller files,
* ``1.00``: best quality images but larger files.

::

    yoga.image.optimize("./input.png", "./output.jpg", options={
        "output_format": "jpeg",
        "jpeg_quality": 0.84,
    })

.. NOTE::

   This option has effect only when the output image is a JPEG.


opacity_threshold
~~~~~~~~~~~~~~~~~

The threshold below which a pixel is considered transparent. This option is
only useful when ``output_format`` is defined to ``auto``.

The value is a number between ``0`` and ``255`` (``254`` by default):

* ``0``: all pixels are considered transparent,
* ``255``: all pixels are considered opaque.

::

    yoga.image.optimize("./input.png", "./output.xxx", options={
        "output_format": "auto",
        "opacity_threshold": 254,
    })


API
---
"""

import io

from PIL import Image
import pyguetzli
import zopfli

from .options import normalize_options
from .helpers import image_have_alpha


def optimize(input_file, output_file, options={}, verbose=False, quiet=False):
    """Optimize given image.

    :param str,file-like input_file: The path of the input image.
    :param str,file-like output_file: The path of the output image.
    :param dict options: Optimization options (see above).
    :param bool verbose: ignored parameter.
    :param bool quiet: ignored parameter.
    """
    options = normalize_options(options)

    image = Image.open(input_file)

    if options["output_format"] == "orig" and image.format not in ("JPEG", "PNG"):                      # noqa
        raise ValueError("The input image must be a JPEG or a PNG when setting 'output_format' to 'orig'")    # noqa

    # resize
    if options["resize"] != "orig":
        image.thumbnail(options["resize"], Image.LANCZOS)

    # output format
    output_format = None

    if options["output_format"] == "orig":
        output_format = image.format.lower()
    elif options["output_format"] in ("jpeg", "png"):
        output_format = options["output_format"]
    else:  # auto
        if image_have_alpha(image, options["opacity_threshold"]):
            output_format = "png"
        else:
            # XXX Maybe we should try to encode in both format
            # and choose the smaller output?
            output_format = "jpeg"

    # convert / optimize
    output_image_bytes = None
    if output_format == "jpeg":
        output_image_bytes = pyguetzli.process_pil_image(
                image, int(options["jpeg_quality"] * 100))
    else:
        image_io = io.BytesIO()
        image.save(image_io, format="PNG", optimize=False)
        image_io.seek(0)
        image_bytes = image_io.read()

        # Optimize using zopflipng
        zopflipng = zopfli.ZopfliPNG()
        zopflipng.lossy_8bit = True
        zopflipng.lossy_transparent = True
        zopflipng.filter_strategies = "01234mepb"
        zopflipng.iterations = 20
        zopflipng.iterations_large = 7
        output_image_bytes = zopflipng.optimize(image_bytes)

    # write to output_file
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    output_file.write(output_image_bytes)
