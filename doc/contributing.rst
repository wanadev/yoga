Contributing
============

Thank you for your interest in YOGA. You will find here all useful information
to contribute.


Questions
---------

If you have any question, you can

* `chat with us <https://discord.gg/BmUkEdMuFp>`_ on Discord,
* or `open an issue <https://github.com/wanadev/yoga/issues>`_ on Github.


Bugs
----

YOGA does not work? Please `open an issue
<https://github.com/wanadev/yoga/issues>`_ on Github with as much information
as possible:

* How you installed YOGA (Git, PyPI, Static build,...),
* What is your operating system / Linux distribution (and its version),
* All the error messages outputted by YOGA,
* ...


Pull Requests
-------------

Please consider `filing a bug <https://github.com/wanadev/yoga/issues>`_
before starting to work on a new feature. This will allow us to discuss the
best way to do it. This is, of course, not necessary if you just want to fix
some typo in the documentation or small errors in the code.

Please note that your code must pass tests and follow the coding style defined
by the `pep8 <https://pep8.org/>`_. The code of this project is automatically
checked by Flake8_ and the coding style is enforced using Black_.


Packaging YOGA
--------------

Build Dependencies
~~~~~~~~~~~~~~~~~~

You will need the following dependencies to build YOGA:

* GCC with C++ 11 support
* GNU Make
* cmake
* Python >= 3.8 (with headers)
* Python setuptools
* Python CFFI

On Debian and Ubuntu this can be installed with the following command::

    sudo apt install build-essential cmake python3 python3-dev python3-setuptools python3-cffi

Downloading the sources
~~~~~~~~~~~~~~~~~~~~~~~

Please download the source from PyPI, not from Github (Assimp sources are missing from Github tarballs)::

    https://files.pythonhosted.org/packages/source/y/yoga/yoga-<VERSION>.tar.gz

Example::

    wget https://files.pythonhosted.org/packages/source/y/yoga/yoga-1.0.0.tar.gz
    tar -xvzf yoga-1.0.0.tar.gz
    cd yoga-1.0.0

Building YOGA
~~~~~~~~~~~~~

Use the following command to build YOGA::

    python3 setup.py build

Installing YOGA
~~~~~~~~~~~~~~~

If your build folder is ``"/tmp/my-package"``, you can install YOGA into it using the following command::

    python3 setup.py install --prefix=/tmp/my-package/usr --optimize=1 --skip-build


Developing YOGA
---------------

If you want to contribute to the YOGA development, you will find here all
useful information to start. Please note that this guide assume you are using
Linux as operating system and a POSIX shell (like Bash or ZSH).

Programming languages used in this project:

* Python_ (3.8 to 3.12)
* C++

Libraries:

* CFFI_: C/Python binding
* imagequant_: Color quantization (to reduce number of colors in an image)
* mozjpeg-lossless-optimization_: Lossless JPEG optimization
* Pillow_: Image processing library
* PyGuetzli_: JPEG optimization
* ZopfliPy_: PNG optimization

Development tools:

* Black_: Code formatter
* Flake8_: Linter
* Pytest_: Unit test
* Codespell_: Code spell

Documentation:

* Sphinx_: Static documentation generator

Installing Prerequisite
~~~~~~~~~~~~~~~~~~~~~~~

**On Linux**, you will need to install Python, cmake and the GCC toolchain to
build the C++ part of YOGA. On Debian / Ubuntu, this can be achieved with the
following command::

    sudo apt install build-essential cmake python3 python3-dev python3-pip python3-venv python-setuptools

**On Windows** you will need to install Python, cmake and Visual Studio Build
Tools (MSVC and MSBuild) and have them available in your PATH. You may find some more information in the ``winbuild/`` folder of the YOGA repository:

* https://github.com/wanadev/yoga/tree/master/winbuild


Creating a Virtualenv
~~~~~~~~~~~~~~~~~~~~~

While not mandatory, using a *virtualenv* is **highly recommended** to avoid
installing dependencies everywhere on your system and to ensure using the right
version of the dependencies.

To create the *virtualenv*, you can use the following command::

    python3 -m venv __env__

This should create a ``__env__/`` folder in the current directory. This is where dependencies will be installed.

Once the *virtualenv* created, you have to activate it with the following command::

    source __env__/bin/activate

This should prefix your prompt with ``(__env__)``.

To leave the *virtualenv*, just type the following command::

    deactivate

If you want to go back in the *virtualenv*, you will only need to execute the
``"source __env__/bin/activate"`` command again.


Installing the Python Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install the development dependencies, just run the following command (with
your *virtualenv* activated)::

    pip install -r requirements.dev.txt


Building the C++ Part of YOGA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building Assimp
"""""""""""""""

You will first need to build *assimp*, the library used by YOGA to handle 3D
models. This can be done with the following command (with your *virtualenv*
activated)::

    python setup.py build

.. NOTE::

   You will not need to run this command again, until you make some
   modification in the Assimp sources (``assimp/`` folder).

Building the YOGA C++ module
""""""""""""""""""""""""""""

To build the YOGA C++ module, run the following command (with your *virtualenv*
activated)::

    python yoga/model/assimp_build.py

This will generate a ``.so`` file (for Linux; on Windows this will be
a ``.pyd`` file instead) in the ``yoga/model/`` folder.

.. NOTE::

   You will not need to run this command again, until you modify the
   ``yoga/model/assimp.cpp`` and ``yoga/model/assimp.h`` files.


Linting and Testing
~~~~~~~~~~~~~~~~~~~

You can check for lint and coding style errors with the following command::

    nox -s lint

If Black reports you coding style errors, you can automatically fix them with
this command::

    nox -s black_fix

To run the tests use::

    nox -s test

To run the tests only for a specific Python version, you can use following
commands (the corresponding Python interpreter must be installed on your
machine)::

    nox -s test-3.8
    nox -s test-3.9
    nox -s test-3.10
    nox -s test-3.11
    nox -s test-3.12

YOGA tests are very slow to run (especially the ones related to the image
optimization). If you want to run only specific tests, you can run them using
pytest_::

    pytest -v test/specific_test_file.py



Building the Documentation
--------------------------

This documentation is build using Sphinx_.

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can run the following command::

    nox -s gendoc


Updating ASSIMP
---------------

ASSIMP is the C++ library used by YOGA to manipulate 3D models. To update it,
first check the latest version tag on the project's repo :

* https://github.com/assimp/assimp/tags

Then go to the assimp subfolder and checkout the latest release tag::

    cd assimp/
    git fetch
    git checkout vX.Y.Z
    cd ..

Then, run tests to ensure YOGA still work::

    nox -s test

Finally, check we are still able to build a wheel from the sdist package::

    nox -s test_build_wheel

If the build fails because of a missing file, add it in ``MANIFEST.in``.


.. _Python: https://www.python.org/

.. _CFFI: https://cffi.readthedocs.io/en/latest/
.. _imagequant: https://github.com/wanadev/imagequant-python
.. _mozjpeg-lossless-optimization: https://github.com/wanadev/mozjpeg-lossless-optimization
.. _Pillow: https://pillow.readthedocs.io/en/stable/
.. _PyGuetzli: https://github.com/wanadev/pyguetzli
.. _ZopfliPy: https://github.com/hattya/zopflipy

.. _Flake8: https://flake8.pycqa.org/en/latest/
.. _Black: https://black.readthedocs.io/en/stable/
.. _pytest: https://docs.pytest.org/
.. _Codespell: https://github.com/codespell-project/codespell

.. _Sphinx: https://www.sphinx-doc.org/en/master/
