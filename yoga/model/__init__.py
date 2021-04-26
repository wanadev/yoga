"""
This module allows to convert and optimize 3D models.


Usage
-----

converting and optimizing a model::

    import yoga.model
    yoga.model.optimize("./input.fbx", "./output.glb")

You can also tune the output by passing options::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        # Model options
        "output_format": "glb",                # "glb"|"gltf"
        "fallback_texture": None,              # None|<FileLike>|"./image.png"
        "no_graph_optimization": False,        # True|False
        "no_meshes_optimization": False,       # True|False
        "no_textures_optimization": False,     # True|False
        "no_fix_infacing_normals": False,      # True|False

        # Images (textures) options
        "image_output_format": "orig",         # "orig"|"auto"|"jpeg"|"png"|"webp"|"webpl"
        "image_resize": "orig",                # "orig"|[width,height]
        "image_jpeg_quality": 0.84,            # 0.00-1.0
        "image_webp_quality": 0.90,            # 0.00-1.0
        "image_opacity_threshold": 254,        # 0-255
        "image_png_slow_optimization": False,  # True|False
    })


Available Model Options
-----------------------

output_format
~~~~~~~~~~~~~

The format of the output model.

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "output_format": "glb",
    })

The following formats are supported:

* ``glb`` (default)
* ``gltf``


fallback_texture
~~~~~~~~~~~~~~~~

This option allows you to provide a fallback texture that will be used when
YOGA is unable to find one of the model textures.

The following values are allowed:

* ``None``: no fallback texture,
* a Python ``str`` (and ``unicode`` for Python 2): path of a fallback image
  file (e.g. ``"./fallback.png"``),
* a "File-like" object (file, ``BytesIO``, etc.).

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "fallback_texture": None,
    })

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "fallback_texture": "./fallback.png",
    })

::

    image_file = open("./fallback.png", "rb")
    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "fallback_texture": image_file,
    })


no_graph_optimization
~~~~~~~~~~~~~~~~~~~~~

Disables empty graph nodes merging.

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "no_graph_optimization": False,
    })


no_meshes_optimization
~~~~~~~~~~~~~~~~~~~~~~

Disable mesh optimization.

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "no_meshes_optimization": False,
    })


no_textures_optimization
~~~~~~~~~~~~~~~~~~~~~~~~

Disable texture optimizations (textures will not be optimized using YOGA
Image).

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "no_textures_optimization": False,
    })


no_fix_infacing_normals
~~~~~~~~~~~~~~~~~~~~~~~~

Disables the assimp's infacing normals fix. This postprocess tries to determine
which meshes have normal vectors that are facing inwards and inverts them. See
the `assimp documentation
<http://assimp.sourceforge.net/lib_html/postprocess_8h.html>`_ for more
details.

::

    yoga.model.optimize("./input.fbx", "./output.glb", options={
        "no_fix_infacing_normals": False,
    })


Available Image Options
-----------------------

YOGA Model optimizes textures using YOGA Images, so there are options
equivalent to the YOGA Image ones available:

* The YOGA Model ``image_output_format`` option is equivalent to the
  ``output_format`` of YOGA Image,

* The YOGA Model ``image_resize`` option is equivalent to the ``resize`` of
  YOGA Image,

* The YOGA Model ``image_jpeg_quality`` option is equivalent to the
  ``jpeg_quality`` of YOGA Image,

* The YOGA Model ``image_webp_quality`` option is equivalent to the
  ``webp_quality`` of YOGA Image,

* The YOGA Model ``image_opacity_threshold`` option is equivalent to the
  ``opacity_threshold`` of YOGA Image,

* The YOGA Model ``image_png_slow_optimization`` option is equivalent to the
  ``png_slow_optimization`` of YOGA Image,

See :ref:`YOGA Image options <yoga_image_api_options>` for more information.


API
---
"""

import sys
import os.path

from .assimp import assimp_import_from_bytes, assimp_export_to_bytes
from .options import normalize_options, extract_image_options
from .helpers import model_embed_images


def optimize(
    input_file,
    output_file,
    options={},
    textures=None,
    verbose=False,
    quiet=False,
):
    """Optimize given model.

    :param str,file-like input_file: The input model file.
    :param str,file-like output_file: The output model file.
    :param dict options: Optimization options (see above).
    :param dict textures: A dictionnary that maps textures path to bytes. When
                          not ``None``, there will be no file system reads in
                          order to find referenced textures. YOGA will look
                          into that dictionary instead.
    :param bool verbose: If ``True``, Assmimp debug message will be print to
                         stdout.
    :param bool quiet: If ``True``, YOGA will not write any warning on stdout
                                    or stderr.

    Example ``textures`` dictionary::

        textures = {
            "images/texture1.png": open("./images/texture1.png", "rb").read(),
            "texture2.png": open("./texture1.png", "rb").read(),
        }
    """

    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    if quiet:
        verbose = False

    # Open file if possible
    if not hasattr(input_file, "read"):
        input_file = open(input_file, "rb")

    root_path = None
    if hasattr(input_file, "name"):
        root_path = os.path.dirname(os.path.abspath(input_file.name))

    if sys.version_info.major == 2 and type(root_path) is str:
        root_path = root_path.decode("utf-8")

    # input_file -> string (path), bytes, file-like
    if hasattr(input_file, "read"):
        input_file = input_file.read()

    # Import the scene
    scene = assimp_import_from_bytes(
        input_file,
        not model_options["no_graph_optimization"],
        not model_options["no_meshes_optimization"],
        not model_options["no_fix_infacing_normals"],
        verbose,
    )

    # Embed images
    # @note We save the bytes to a dictionnary so that the garbage collector
    # does not occur before exporting the scene a bit later
    images_bytes = {}
    model_embed_images(
        scene["cffi_pointer"].images,
        images_bytes,
        not model_options["no_textures_optimization"],
        model_options["fallback_texture"],
        root_path,
        image_options,
        textures,
        quiet,
    )

    # Export the scene
    bytes_out = assimp_export_to_bytes(
        scene["cffi_pointer"],
        model_options["output_format"],
    )

    # Write to output
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    output_file.write(bytes_out)
