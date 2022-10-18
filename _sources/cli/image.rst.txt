YOGA Image Command Line Interface
=================================

.. code-block:: text

    usage: yoga image [-h] [-v] [-q] [--output-format {orig,auto,jpeg,png}]
                      [--resize {orig,<SIZE>,<WIDTH>x<HEIGHT>}] [--jpeg-quality 0-100]
                      [--opacity-threshold 0-255]
                      input output

    positional arguments:
      input                 Input file path
      output                Output file path

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         enable verbose mode
      -q, --quiet           enable quiet mode (takes precedence over verbose)
      --output-format {orig,auto,jpeg,png,webp,webpl}
                            format of the output image
      --resize {orig,<SIZE>,<WIDTH>x<HEIGHT>}
                            resize the image
      --jpeg-quality 0-100  JPEG quality if the output format is set to 'jpeg'
      --webp-quality 0-100  WEBP quality if the output format is set to 'webp'
      --opacity-threshold 0-255
                            threshold below which a pixel is considered transparent
      --png-slow-optimization
                            enable a (very) slow optimization preset for PNGs that
                            can sometimes gain few bytes on the output file
      --enable-quantization
                            reduce the number of colors used in the image
      --quantization-dithering-level 0.0-1.0
                            the dithering level to use when
                            --enable-quantization is set
      --quantization-max-colors 1-256
                            the maximum number of colors to use when
                            --enable-quantization is set



Basic Usage
-----------

The simplest way to optimize an image is by using the following command::

    yoga  image  input.png  output.png

.. NOTE::

   When the output format is not specified, YOGA outputs an image using the same format as the input one (``PNG`` → ``PNG``, ``JPEG`` → ``JPEG``, ``WEBP`` → ``WEBP``, ``WEBP (lossless)`` → ``WEBP (lossless)``).

   Only PNGs, JPEGs and WEBPs are supported as input when the output format is not explicitly specified.


Output Format
-------------

The output format can be specified using the ``--output-format`` option::

    yoga  image  --ouput-format=jpeg   input.png  output.jpg

The following formats are supported:

* ``orig``: This is the default. The output format will be the same as the one of the input image.
* ``auto``: The output format is automatically selected. YOGA will generate a PNG if the input image is using transparency, else it will generate a JPEG.
* ``png``: Outputs a PNG image.
* ``jpeg``: Outputs a JPEG image.
* ``webp``: Outputs a lossy WEBP image.
* ``webpl``: Outputs a lossless WEBP image.

.. NOTE::

   When using the ``"orig"`` output format, YOGA will only accept PNG, JPEG and WEBP images as input.


Resize Output Image
-------------------

YOGA allows you to resize images with the ``--resize`` option::

    yoga  image  --resize=512  input.png  output.png
    yoga  image  --resize=512x512  input.png  output.png

.. NOTE::

   If the width and the height have the same value, you do not have to specify both, so ``512`` and ``512x512`` are equivalent.

.. NOTE::

   YOGA always preserve the image's aspect ratio; you can consider the size you provide as a box the image will fit in.


Output JPEG Quality
-------------------

YOGA allows you to tune the desired quality of the JPEG it outputs with the ``--jpeg-quality`` option. This option takes an integer between ``0`` and ``100`` as parameter:

* ``0``: ugly images but smaller files,
* ``100``: best quality images but larger files.

The default JPEG quality is ``84%``.

::

    yoga  image  --output-format=jpeg  --jpeg-quality=84  input.png  output.jpg

.. NOTE::

   This option has effect only when the output image is a JPEG.


Output WEBP Quality
-------------------

YOGA allows you to tune the desired quality of the WEBP it outputs with the ``--webp-quality`` option. This option takes an integer between ``0`` and ``100`` as parameter:

* ``0``: ugly images but smaller files,
* ``100``: best quality images but larger files.

The default WEBP quality is ``90%``.

::

    yoga  image  --output-format=webp  --webp-quality=90  input.png  output.webp

.. NOTE::

   This option has effect only when the output image is a lossy WEBP.


Opacity Threshold
-----------------

YOGA allows you to tune the threshold below which a pixel is considered transparent using the ``--opacity-threshold`` option. This option is only useful in addition to ``--output-format=auto`` and takes an integer between ``0`` and ``255`` as parameter:

* ``0``: all pixels are considered transparent,
* ``255``: all pixels are considered opaque.

The default value is ``254``.

::

    yoga  image  --output-format=auto  --opacity-threshold=254  input.png  output.xxx


Slow PNG Optimization
---------------------

YOGA allows you to select an alternative preset for PNGs optimization. This preset can sometimes gain few bytes over the default one, but it is 10 times slower on average. You will generally not want to enable this.

To enable this preset, use the ``--png-slow-optimization`` option::

    yoga  image  --png-slow-optimization  input.png  output.png


.. _yoga_image_cli_quantization:

Color Quantization
------------------

Color quantization is an operation that reduces the number of distinct colors used in an image.

To enable the color quantization, use the ``--enable-quantization`` option::

    yoga  image  --enable-quantization  input.png  output.png

When color quantization is enabled, YOGA will produce images containing at most 256 colors (8-bit). You can control the maximum number of colors with the ``--quantization-max-colors`` option. This options takes an integer between ``1`` and ``256`` as parameter (``256`` is the default value)::

    yoga  image  --enable-quantization  --quantization-max-colors=128  input.png  output.png

By default, YOGA will use dithering to reduce the visual impact of the color loss, but this have an incidence on the efficiency of the compression. You can control the level of the dithering or disable it using the ``--quantization-dithering-level`` option, that takes a number between ``0.0`` and ``1.0`` as value:

* ``0.0``: no dithering
* ``1.0``: maximal dithering

The default value is ``1.0``.

::

    yoga  image  --enable-quantization  --quantization-dithering-level=0.5  input.png  output.png


Here are examples of the effect of the dithering levels:

+---------+------------+----------------------------+-----------+
| Preview | max-colors | dithering-level            | File size |
+=========+============+============================+===========+
| |orig|  | Original image (quantization disabled)  | 7,2 kB    |
+---------+------------+----------------------------+-----------+
| |d1.0|  | 5          | 1.0                        | 1.4 kB    |
+---------+------------+----------------------------+-----------+
| |d0.75| | 5          | 0.75                       | 1.4 kB    |
+---------+------------+----------------------------+-----------+
| |d0.5|  | 5          | 0.5                        | 1.2 kB    |
+---------+------------+----------------------------+-----------+
| |d0.25| | 5          | 0.25                       | 626 B     |
+---------+------------+----------------------------+-----------+
| |d0.0|  | 5          | 0.0                        | 180 B     |
+---------+------------+----------------------------+-----------+

.. |orig| image:: ./images/dithering-original-image.png
   :width: 150px
.. |d1.0| image:: ./images/dithering-1.0-colors-5.png
   :width: 150px
.. |d0.75| image:: ./images/dithering-0.75-colors-5.png
   :width: 150px
.. |d0.5| image:: ./images/dithering-0.5-colors-5.png
   :width: 150px
.. |d0.25| image:: ./images/dithering-0.25-colors-5.png
   :width: 150px
.. |d0.0| image:: ./images/dithering-0.0-colors-5.png
   :width: 150px

.. NOTE::

    In some cases, like PNG to PNG optimisation, the quantization can be
    ignored by YOGA if it produces an output image larger that the input one.
