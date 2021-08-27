Command Line Interface
======================

.. code-block:: text

    usage: yoga [-h] {image,model} [options...] input output

    positional arguments:
      {image,model}
        image        Converts and optimizes images
        model        Converts and optimizes 3D models

    optional arguments:
      -h, --help     show this help message and exit
      --version      show program's version number and exit


The YOGA command line interface is divided in two sub-commands:

* ``yoga image`` to convert and optimize images,
* ``yoga model`` to convert and optimize 3D models.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./image.rst
   ./model.rst
