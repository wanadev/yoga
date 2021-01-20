Welcome to YOGA's documentation!
================================

.. figure:: https://github.com/wanadev/yoga/raw/master/logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG and PNG,
* convert and optimize 3D models from various formats to `GLB`_.

**Images** are opened using Pillow_ and optimized using Guetzli_ (for JPEGs) and
Zopflipng_ (for PNGs).

**3D Models** are converted and optimized using assimp_. If models contain or
reference images, they are processed by YOGA's image optimizer.

.. _GLB: https://www.khronos.org/gltf/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Guetzli: https://github.com/google/guetzli
.. _Zopflipng: https://github.com/google/zopfli
.. _assimp: https://github.com/assimp/assimp

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./install.rst
   ./cli/index.rst
   ./python/index.rst
   ./contributing.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
