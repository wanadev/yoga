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


Developing YOGA
---------------

If you want to contribute to the YOGA development, you will find here all
useful information to start. Please note that this guide assume you are using
Linux as operating system and a POSIX shell (like Bash or ZSH).

Programming languages used in this project:

* Python_ (2.7, 3.7, 3.8 and 3.9)
* C++

Libraries:

* CFFI_: C/Python binding
* Pillow_: Image processing library
* PyGuetzli_: JPEG optimization
* ZopfliPy_: PNG Optimization

Development tools:

* Black_: Code formater
* Flake8_: Linter
* Pytest_: Unit test

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
   modification in the Assmimp sources (``assimp/`` folder).

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

    nox -s test-2.7
    nox -s test-3.7
    nox -s test-3.8
    nox -s test-3.9

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


.. _Python: https://www.python.org/

.. _CFFI: https://cffi.readthedocs.io/en/latest/
.. _Pillow: https://pillow.readthedocs.io/en/stable/
.. _PyGuetzli: https://github.com/wanadev/pyguetzli
.. _ZopfliPy: https://github.com/hattya/zopflipy

.. _Flake8: https://flake8.pycqa.org/en/latest/
.. _Black: https://black.readthedocs.io/en/stable/
.. _pytest: https://docs.pytest.org/

.. _Sphinx: https://www.sphinx-doc.org/en/master/
