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
      --output-format {orig,auto,jpeg,png}
                            format of the output image
      --resize {orig,<SIZE>,<WIDTH>x<HEIGHT>}
                            resize the image
      --jpeg-quality 0-100  JPEG quality if the output format is set to 'jpeg'
      --opacity-threshold 0-255
                            threshold below which a pixel is considered transparent


Basic Usage
-----------

The simplest way to optimize an image is by using the following command::

    yoga  image  input.png  output.png

.. NOTE::

   When the output format is not specified, YOGA outputs an image using the same format as the input one (``PNG`` → ``PNG``, ``JPEG`` → ``JPEG``).

   Only PNGs and JPEGs are supported as input when the output format is not explicitly specified.


Output Format
-------------

The output format can be specified using the ``--output-format`` option::

    yoga  image  --ouput-format=jpeg   input.png  output.jpg

The following formats are supported:

* ``orig``: This is the default. The output format will be the same as the one of the input image.
* ``auto``: The output format is automatically selected. YOGA will generate a PNG if the input image is using transparency, else it will generate a JPEG.
* ``png``: Outputs a PNG image.
* ``jpeg``: Outputs a JPEG image.

.. NOTE::

   When using the ``"orig"`` output format, YOGA will only accept PNGs and JPEGs images as input.


Resize Output Image
-------------------

YOGA allows you to resize images with the ``--resize`` option::

    yoga  image  --resize=512  input.png  ouput.png
    yoga  image  --resize=512x512  input.png  ouput.png

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


Opacity Threshold
-----------------

YOGA allows you to tune the threshold below which a pixel is considered transparent using the ``--opacity-threshold`` option. This option is only useful in addition to ``--output-format=auto`` and takes an integer between ``0`` and ``255`` as parameter:

* ``0``: all pixels are considered transparent,
* ``255``: all pixels are considered opaque.

The default value is ``254``.

::

    yoga  image  --output-format=auto  --opacity-threshold=254  input.png  output.xxx
