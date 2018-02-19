YOGA - Yummy Optimizer for Gorgeous Assets
==========================================

.. figure:: ./logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG and PNG,
* convert and optimize 3D models from various formats to `glTF and GLB`_.
  **(NOT YET IMPLEMENTED)**

**Images** are opened using Pillow_ and optimized using Guetzli_ (for JPEGs) and
Zopflipng_ (for PNGs).

**3D Models** are converted and optimized using assimp_. If models contain or
reference images, they are processed by YOGA's image optimizer.

Convert and optimize an image from CLI::

    yoga  image  input.png  output.png
    yoga  image  --output-format=jpeg  --jpeg-quality=84  input.png  output.jpg
    yoga  image  --help

Convert and optimize a 3D model from CLI::

    # TODO (not implemented yet)
    yoga  model  --help

.. _glTF and GLB: https://www.khronos.org/gltf/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Guetzli: https://github.com/google/guetzli
.. _Zopflipng: https://github.com/google/zopfli
.. _assimp: https://github.com/assimp/assimp


Changelog
---------

* **0.9.0-beta1:** First release (only GLB output for models, no image auto
  output format)
