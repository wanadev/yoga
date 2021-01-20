Contributing
============

Thank you for your interest in YOGA. You will find here all useful information
to contribute.


Questions
---------

If you have any question, you can `open an issue
<https://github.com/wanadev/yoga/issues>`_ on Github.


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
by the `pep8 <https://pep8.org/>`_.


Running the Tests
-----------------

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can check for lint error::

    nox --session lint

or run the tests::

    nox --session test

To run the tests only for a specific Python version, you can use following
commands (the corresponding Python interpreter must be installed on your
machine)::

    nox --session test-2.7
    nox --session test-3.5
    nox --session test-3.6
    nox --session test-3.7
    nox --session test-3.8
    nox --session test-3.9


Building the Documentation
--------------------------

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can run the following command::

    nox --session gendoc
