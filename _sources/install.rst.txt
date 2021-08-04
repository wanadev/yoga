Installing YOGA
===============

From PyPI
---------

To install YOGA from PyPI, just run the following command (as ``root`` on Linux)::

    pip3 install yoga

.. NOTE::

    We provide precompiled YOGA packages for most common platforms. You may need to install additional build dependencies if there is no precompiled package available for your platform (see below).


From Sources
------------

To install YOGA from sources, you will have to install some build dependencies first.

On Debian / Ubuntu, you can install everything you need using the following command::

   sudo apt install build-essential cmake python3 python3-dev python3-pip python3-setuptools

Then clone the repository::

    git clone https://github.com/wanadev/yoga.git

Go to the project's directory::

    cd yoga

Get the submodules::

    git submodule init
    git submodule update

Build and install using the following command (as ``root`` on Linux)::

    python3 setup.py install

.. NOTE::

    On "exotic" platforms (a.k.a. old systems, non-intel machines, distribution
    that do not use libc6 (like Alpine that uses Musl),...) you may have to
    also compile YOGA's dependencies. Here are some links to their respective
    documentations:

    * `Building Pillow from sources <https://pillow.readthedocs.io/en/stable/installation.html#building-from-source>`_
    * `Installing PyGuetzli from sources <https://wanadev.github.io/pyguetzli/install.html#installing-from-source>`_
    * `ZopfliPy documentation <https://github.com/hattya/zopflipy>`_ (only basic build dependencies seems to be required)


Windows Standalone Releases
---------------------------

The simplest way to use YOGA on Windows is to download the latest standalone build here:

* https://github.com/wanadev/yoga/releases
