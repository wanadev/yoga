YOGA - Yummy Optimizer for Gorgeous Assets
==========================================

.. figure:: ./logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG and PNG,
* *convert and optimize 3D models from various formats to gLTF and GLB.* **NOT YET IMPLEMENTED**

Images are opened using Pillow and optimized using Guetzli (for JPEGs) and
Zopflipng (for PNGs).

3D Models are converted and optimized using ASSIMP. If models contain or
reference images, they are processed by YOGA's image optimizer.

Convert and optimize an image from CLI::

    yoga  image  input.png  output.png
    yoga  image  --output-format=jpeg  --jpeg-quality=84  input.png  output.jpg
    yoga  image  --help

Convert and optimize a 3D model from CLI::

    # TODO (not implemented yet)
    yoga  model  --help
