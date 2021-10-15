YOGA - Yummy Optimizer for Gorgeous Assets
==========================================

|Github| |Discord| |PYPI Version| |Build Status| |Black| |License|

.. figure:: https://github.com/wanadev/yoga/raw/master/logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG, PNG and WEBP,
* convert and optimize 3D models from various formats to `glTF and GLB`_.

**Images** are opened using Pillow_ and optimized using Guetzli_ (for JPEGs),
Zopflipng_ (for PNGs) and libwebp_ (for WEBPs).

**3D Models** are converted and optimized using assimp_. If models contain or
reference images, they are processed by YOGA's image optimizer.

EXAMPLE: Converting and optimizing an image from CLI::

    yoga  image  input.png  output.png
    yoga  image  --output-format=jpeg  --jpeg-quality=84  input.png  output.jpg
    yoga  image  --help

EXAMPLE: Converting and optimizing a 3D model from CLI::

    yoga  model  input.fbx  output.glb
    yoga  model  --no-graph-optimization  --no-meshes-optimization  --image-output-format=jpeg  --image-jpeg-quality=84  input.fbx  output.glb
    yoga  model  --help

.. _glTF and GLB: https://www.khronos.org/gltf/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Guetzli: https://github.com/google/guetzli
.. _Zopflipng: https://github.com/google/zopfli
.. _libwebp: https://chromium.googlesource.com/webm/libwebp/
.. _assimp: https://github.com/assimp/assimp


Install
-------

* See `the install section of the documentation <https://wanadev.github.io/yoga/install.html>`_


Documentation
-------------

* `Command Line Interface (CLI) <https://wanadev.github.io/yoga/cli/index.html>`_
* `Python API <https://wanadev.github.io/yoga/python/index.html>`_
* `Contributing <https://wanadev.github.io/yoga/contributing.html>`_


Changelog
---------

* **[NEXT]** (changes on ``master`` that have not been released yet):

  * Nothing yet...

* **1.1.2:**

  * Add flag to CFFI builder to fix MacOS build

* **1.1.1 (not published):**

  * JPEG: ignore invalid values for the orientation tag (#38)
  * Python 3.10 support and wheels

* **1.1.0:**

  * **JPEG Optimization:**

    * Honor the JPEG orientation EXIF tag
    * JPEG optimization has been improved by using some optimizations from
      MozJPEG after the Guetzli encoding (from 2.4 % to 7.3 % of additional size
      reduction)

  * **PNG Optimization:**

    * YOGA can no more output a PNG larger than the input one when performing
      a PNG to PNG optimization

  * **CLI:**

    * Allow to cancel an optimization using Ctrl+C (NOTE: may not work on
      Windows)
    * Add a ``--version`` option to get YOGA's version
    * Improve ``yoga --help`` usage

  * **Python versions:**

    * Python 2.7 support dropped

  * **NOTE for packagers:**

    * new dependency to `mozjpeg-lossless-optimization
      <https://github.com/wanadev/mozjpeg-lossless-optimization>`_

* **1.0.0:**

  * WEBP (lossy and lossless) images supported as output format
  * PNG default optimization preset changed to a 10× faster preset (old preset
    stil available with ``--png-slow-optimization`` flag)
  * New model flag ``--no-fix-infacing-normals`` to disable Assimp's "fix
    infacing normals" postprocess (#32, #33)
  * Show CLI usage when no parameter given
  * Developer documentation improved (#31)
  * ASSIMP library updated
  * WARNING: This is the last version to actively support Python 2.7!

* **0.11.1:**

  * Automated workflow for deploying the PyPI packages
  * Wheel are now distributed on PyPI

* **0.11.0:**

  * Allows to build YOGA on Windows
  * Scripts and workflow to build Windows standalone versions

* **0.10.2:**

  * Updates assimp and python libraries

* **0.10.1:**

  * Fixes an issue that occures when output file does not already exist

* **0.10.0:**

  * Prevent overwriting of the output file when an error occurs (#17)
  * Unicode path support (#16)

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


.. |Github| image:: https://img.shields.io/github/stars/wanadev/yoga?label=Github&logo=github
   :target: https://github.com/wanadev/yoga
.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/BmUkEdMuFp
.. |PYPI Version| image:: https://img.shields.io/pypi/v/yoga.svg
   :target: https://pypi.python.org/pypi/yoga
.. |Build Status| image:: https://github.com/wanadev/yoga/workflows/Python%20CI/badge.svg
   :target: https://github.com/wanadev/yoga/actions
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/
.. |License| image:: https://img.shields.io/pypi/l/yoga.svg
   :target: https://github.com/wanadev/yoga/blob/master/LICENSE
