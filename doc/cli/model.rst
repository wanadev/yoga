YOGA Model Command Line Interface
=================================

.. code-block:: text

    usage: yoga model [-h] [-v] [-q] [--output-format {glb,gltf}] [--fallback-texture <PATH>]
                      [--no-graph-optimization] [--no-meshes-optimization]
                      [--no-textures-optimization] [--image-output-format {orig,auto,jpeg,png}]
                      [--image-resize {orig,<SIZE>,<WIDTH>x<HEIGHT>}]
                      [--image-jpeg-quality 0-100] [--image-opacity-threshold 0-255]
                      input output

    positional arguments:
      input                 Input file path
      output                Output file path

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         enable verbose mode
      -q, --quiet           enable quiet mode (takes precedence over verbose)

    model options:
      --output-format {glb,gltf}
                            format of the output model (default: glb)
      --fallback-texture <PATH>
                            fallback image used when unable to find a texture
      --no-graph-optimization
                            disable empty graph nodes merging
      --no-meshes-optimization
                            disable meshes optimization
      --no-textures-optimization
                            disable textures optimization using yoga image
      --no-fix-infacing-normals
                            disable fix infacing normals

    image options:
      --image-output-format {orig,auto,jpeg,png,webp,webpl}
                            format of the output image
      --image-resize {orig,<SIZE>,<WIDTH>x<HEIGHT>}
                            resize the image
      --image-jpeg-quality 0-100
                            JPEG quality if the output format is set to 'jpeg'
      --image-webp-quality 0-100
                            WEBP quality if the output format is set to 'webp'
      --image-opacity-threshold 0-255
                            threshold below which a pixel is considered transparent
      --image-png-slow-optimization
                            enable a (very) slow optimization preset for PNGs that
                            can sometimes gain few bytes on the output file
      --image-enable-quantization
                            reduce the number of colors used in the image
      --image-quantization-dithering-level 0.0-1.0
                            the dithering level to use when
                            --image-enable-quantization is set
      --image-quantization-max-colors 1-256
                            the maximum number of colors to use when
                            --image-enable-quantization is set




Basic Usage
-----------

To convert and optimize a 3D model using YOGA, you can use the following command::

    yoga  model  input.fbx  output.glb


Output Format
-------------

You can choose the output format between one of the two that are supported using the ``--output-format`` option::

    yoga  model  --output-format=glb  input.fbx  output.glb

The supported output formats are:

* ``glb`` (default),
* ``gltf``.


Disabling Optimizations
-----------------------

By default, YOGA optimize the 3D models and its textures. The optimizations can be disabled using the following options:

* ``--no-graph-optimization``: disables empty graph nodes merging,
* ``--no-meshes-optimization``: disable mesh optimization,
* ``--no-textures-optimization``: disable texture optimizations (textures will not be optimized using YOGA Image).

::

    yoga  model  --no-graph-optimization  --no-meshes-optimization  --no-textures-optimization  input.fbx  output.glb


Disabling Postprocesses
-----------------------

By default, YOGA use several postprocesses, some can be disabled using the following options:

* ``--no-fix-infacing-normals``: disable the "fix infacing normals"
  postprocess. This postprocess tries to determine which meshes have normal
  vectors that are facing inwards and inverts them. See the `assimp
  documentation <http://assimp.sourceforge.net/lib_html/postprocess_8h.html>`_
  for more details.

::

    yoga  model  --no-fix-infacing-normals  input.fbx  output.glb


Images Options
--------------

YOGA Model optimizes textures using YOGA Images, so there are options equivalent to the YOGA Image ones available:

* The YOGA Model ``--image-output-format`` option is equivalent to the ``--output-format`` of  YOGA Image,

* The YOGA Model ``--image-resize`` option is equivalent to the ``--resize`` of  YOGA Image,

* The YOGA Model ``--image-jpeg-quality`` option is equivalent to the ``--jpeg-quality`` of  YOGA Image,

* The YOGA Model ``--image-webp-quality`` option is equivalent to the ``--webp-quality`` of  YOGA Image,

* The YOGA Model ``--image-opacity-threshold`` option is equivalent to the ``--opacity-threshold`` of  YOGA Image,

* The YOGA Model ``--image-png-slow-optimization`` option is equivalent to the ``--png-slow-optimization`` of  YOGA Image,

* The YOGA Model ``--image-enable-quantization`` option is equivalent to the ``--enable-quantization`` of  YOGA Image,

* The YOGA Model ``--image-quantization-dithering-level`` option is equivalent to the ``--quantization-dithering-level`` of  YOGA Image,

* The YOGA Model ``--image-quantization-max-colors`` option is equivalent to the ``--quantization-max-colors`` of  YOGA Image,

See the :doc:`./image` documentation for more information.
