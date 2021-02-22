Welcome to YOGA's documentation!
================================

|Github| |Discord| |PYPI Version| |Build Status| |License|

.. figure:: https://github.com/wanadev/yoga/raw/master/logo.png
   :alt:

**YOGA** is a command-line tool and a library that can:

* convert and optimize images from various format to JPEG and PNG,
* convert and optimize 3D models from various formats to `glTF and GLB`_.

**Images** are opened using Pillow_ and optimized using Guetzli_ (for JPEGs) and
Zopflipng_ (for PNGs).

**3D Models** are converted and optimized using assimp_. If models contain or
reference images, they are processed by YOGA's image optimizer.

.. _glTF and GLB: https://www.khronos.org/gltf/
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



.. |Github| image:: https://img.shields.io/github/stars/wanadev/yoga?label=Github&logo=github
   :target: https://github.com/wanadev/yoga
.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/BmUkEdMuFp
.. |PYPI Version| image:: https://img.shields.io/pypi/v/yoga.svg
   :target: https://pypi.python.org/pypi/yoga
.. |Build Status| image:: https://github.com/wanadev/yoga/workflows/Python%20CI/badge.svg
   :target: https://github.com/wanadev/yoga/actions
.. |License| image:: https://img.shields.io/pypi/l/yoga.svg
   :target: https://github.com/wanadev/yoga/blob/master/LICENSE