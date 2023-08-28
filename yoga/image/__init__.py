"""
This module allows to convert and optimize images.

Usage
-----

Converting and optimizing an image::

    import yoga.image
    yoga.image.optimize("./input.png", "./output.png")

You can also tune the output by passing options::

    yoga.image.optimize("./input.png", "./output.png", options={
        "output_format": "orig",         # "orig"|"auto"|"jpeg"|"png"|"webp"|"webpl"
        "resize": "orig",                # "orig"|[width,height]
        "jpeg_quality": 0.84,            # 0.00-1.0
        "webp_quality": 0.90,            # 0.00-1.0
        "opacity_threshold": 254,        # 0-255
        "png_slow_optimization": False,  # True|False
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
* ``webp`` Outputs a lossy WEBP image.
* ``webpl`` Outputs a lossless WEBP image.

.. NOTE::

   When using the ``"orig"`` output format, YOGA will only accept PNG, JPEG and
   WEBP images as input.


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


webp_quality
~~~~~~~~~~~~

The quality of the output WEBPs.

The value is a number between ``0.00`` and ``1.00`` (``0.90`` by default):

* ``0.00``: ugly images but smaller files,
* ``1.00``: best quality images but larger files.

::

    yoga.image.optimize("./input.png", "./output.webp", options={
        "output_format": "webp",
        "webp_quality": 0.90,
    })

.. NOTE::

   This option has effect only when the output image is a lossy WEBP.


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


png_slow_optimization
~~~~~~~~~~~~~~~~~~~~~

If ``True``, select a slower optimization preset for PNGs. This preset can
sometimes gain few bytes over the default one, but it is 10 times slower on
average.

You will generally not want to enable this.

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "output_format": "png",
        "png_slow_optimization": False,
    })


enable_quantization
~~~~~~~~~~~~~~~~~~~

If ``True``, YOGA will reduce the number of distinct colors used in the image
to 256 colors maximum. By default dithering will be used to reduce the visual
impact of the color loss.

The color quantization is disabled by default.

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "enable_quantization": True,
    })


See :ref:`yoga_image_cli_quantization` CLI options for more details.


quantization_max_colors
~~~~~~~~~~~~~~~~~~~~~~~

The maximum number of colors to use in the output image. This options has
effect only when ``enable_quantization`` is set to ``True``.

The value is a number between ``1`` and ``256`` (``256`` by default).

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "enable_quantization": True,
        "quantization_max_colors": 256,
    })

See :ref:`yoga_image_cli_quantization` CLI options for more details.


quantization_dithering_level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The maximum dithering level used when reducing image colors. This options has
effect only when ``enable_quantization`` is set to ``True``.

The value is a number between ``0.0`` and ``1.0`` (``1.0`` by default):

* ``0.0``: no dithering
* ``1.0``: maximal dithering

::

    yoga.image.optimize("./input.png", "./output.png", options={
        "enable_quantization": True,
        "quantization_dithering_level": 1.0,
    })

See :ref:`yoga_image_cli_quantization` CLI options for more details.


API
---
"""

from PIL import Image
from imagequant import quantize_pil_image

from .encoders.jpeg import optimize_jpeg
from .encoders.jpeg import open_jpeg
from .encoders.png import optimize_png
from .encoders.webp import optimize_lossy_webp
from .encoders.webp_lossless import optimize_lossless_webp
from .options import normalize_options
from . import helpers


# Since Pillow v9.1.0, constants on the Image object are deprecated and will be
# removed in Pillow v10.0.0. This code ansure the compatibility with all
# versions.
# See: https://pillow.readthedocs.io/en/stable/deprecations.html#constants
Resampling = Image
if hasattr(Image, "Resampling"):
    Resampling = Image.Resampling


def optimize(input_file, output_file, options={}, verbose=False, quiet=False):
    """Optimize given image.

    :param str,file-like input_file: The path of the input image.
    :param str,file-like output_file: The path of the output image.
    :param dict options: Optimization options (see above).
    :param bool verbose: ignored parameter.
    :param bool quiet: ignored parameter.
    """
    options = normalize_options(options)

    # Image as file-like object
    if isinstance(input_file, str):
        image_file = open(input_file, "rb")
    elif hasattr(input_file, "read") and hasattr(input_file, "seek"):
        image_file = input_file
    else:
        raise ValueError("Unsupported parameter type for 'input_file'")

    # Get raw image data
    raw_data = image_file.read()
    image_file.seek(0)  # to allow PIL.Image to read the file

    # Determine the input image format
    try:
        input_format = helpers.guess_image_format(raw_data)
    except ValueError:
        input_format = None

    # Open the image with Pillow
    if input_format == "jpeg":
        image = open_jpeg(image_file)
    else:
        image = Image.open(image_file)

    # Resize image if requested
    if options["resize"] != "orig":
        image.thumbnail(options["resize"], Resampling.LANCZOS)

    # Quantize if requested
    if options["enable_quantization"]:
        image = quantize_pil_image(
            image,
            dithering_level=options["quantization_dithering_level"],
            max_colors=options["quantization_max_colors"],
        )

    # Output format
    if options["output_format"] == "orig":
        if input_format is None:
            raise ValueError("Unsupported image format")
        output_format = input_format
    elif options["output_format"] == "auto":
        if helpers.image_have_alpha(image, options["opacity_threshold"]):
            output_format = "png"
        else:
            # XXX Maybe we should try to encode in both format and choose the
            # smaller output?
            output_format = "jpeg"
    else:
        output_format = options["output_format"]

    # Convert / Optimize
    if output_format == "jpeg":
        output_image_bytes = optimize_jpeg(image, options["jpeg_quality"])
    elif output_format == "png":
        output_image_bytes = optimize_png(
            image, raw_data, options["png_slow_optimization"]
        )
    elif output_format == "webp":
        output_image_bytes = optimize_lossy_webp(
            image, options["webp_quality"]
        )
    elif output_format == "webpl":
        output_image_bytes = optimize_lossless_webp(image)

    # Write to output_file
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")
        output_file.write(output_image_bytes)
        output_file.close()
    else:
        output_file.write(output_image_bytes)

    # Close input file if we opened it
    if type(input_file) is str:
        image_file.close()
