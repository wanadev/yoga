YOGA - Yummy Optimizer for Gorgeous Assets
==========================================

|Build Status| |PYPI Version| |License| |Gitter|

.. figure:: https://github.com/wanadev/yoga/raw/master/logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG and PNG,
* convert and optimize 3D models from various formats to `GLB`_.

**Images** are opened using Pillow_ and optimized using Guetzli_ (for JPEGs) and
Zopflipng_ (for PNGs).

**3D Models** are converted and optimized using assimp_. If models contain or
reference images, they are processed by YOGA's image optimizer.

Convert and optimize an image from CLI::

    yoga  image  input.png  output.png
    yoga  image  --output-format=jpeg  --jpeg-quality=84  input.png  output.jpg
    yoga  image  --help

Convert and optimize a 3D model from CLI::

    yoga  model  input.fbx  output.glb
    yoga  model  --no-graph-optimization  --no-meshes-optimization  --image-output-format=jpeg  --image-jpeg-quality=84  input.fbx  output.glb
    yoga  model  --help

.. _GLB: https://www.khronos.org/gltf/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Guetzli: https://github.com/google/guetzli
.. _Zopflipng: https://github.com/google/zopfli
.. _assimp: https://github.com/assimp/assimp


Changelog
---------

* **0.10.0:**

  * Prevent overwriting of the output file when an error occurs (#17).
  * Uniode path support

* **0.10.0b1:**

  * Verbose and quiet modes,
  * Allows to pass textures from memory instead of looking on the filesystem,
  * Allows to pass a fallback texture instead of raising an error.

* **0.9.1b1:**

  * Automatic selection of the output format (png or jpeg),
  * Prevent duplication of textures that are shared between materials,
  * Fixes Windows paths of textures.

* **0.9.0b1:** First release (only GLB output for models, no image auto
  output format)


.. |Build Status| image:: https://travis-ci.org/wanadev/yoga.svg?branch=master
   :target: https://travis-ci.org/wanadev/yoga
.. |PYPI Version| image:: https://img.shields.io/pypi/v/yoga.svg
   :target: https://pypi.python.org/pypi/yoga
.. |License| image:: https://img.shields.io/pypi/l/yoga.svg
   :target: https://github.com/wanadev/yoga/blob/master/LICENSE
.. |Gitter| image:: https://badges.gitter.im/gitter.svg
   :target: https://gitter.im/wanadev/yoga
