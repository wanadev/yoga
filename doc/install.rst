Installing YOGA
===============

Linux (Sources)
---------------

To install YOGA from sources, you will have to install some build dependencies first.

On Debian / Ubuntu, you can install everything you need using the following command::

   sudo apt install build-essential cmake python3 python3-dev python3-pip python-setuptools


From PyPI
~~~~~~~~~

To install YOGA from PyPI following command (as ``root`` on Linux)::

    pip3 install yoga


From this repository
~~~~~~~~~~~~~~~~~~~~

Then clone the repository::

    git clone https://github.com/wanadev/yoga.git

Go to the project's directory::

    cd yoga

Build and install using the following command::

    python3 setup.py install


Windows
-------

Windows Standalone Releases
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest way to use YOGA on Windows is to download the latest standalone build here:

* https://github.com/wanadev/yoga/releases

.. NOTE::

   You will have to install Microsoft Visual C++ Redistribuable for Visual
   Studio 2019 to run YOGA. You will find more information in the Zip you
   downloaded or in `this document
   <https://github.com/wanadev/yoga/blob/master/winbuild/README-windows-dist.md>`_.


Building YOGA on Windows
~~~~~~~~~~~~~~~~~~~~~~~~

If you need YOGA as a library or if you really want to build it yourself, look
in the `winbuild/ folder of the source repository
<https://github.com/wanadev/yoga/tree/master/winbuild>`_
folder.
