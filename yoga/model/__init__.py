import sys
import os.path

from .assimp import (assimp_import_from_bytes, assimp_export_to_bytes)
from .options import (normalize_options, extract_image_options)
from .helpers import model_embed_images


def optimize(input_file, output_file, options={}, textures=None,
             verbose=False, quiet=False):
    # TODO: Make a effective documentation.
    # The textures arguments should be a dictionary that maps
    # paths to bytes. When not None, there will be no file system
    # reads in order to find referenced textures. We will
    # look into that dictionary instead.

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
        verbose
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
        quiet
        )

    # Export the scene
    bytes_out = assimp_export_to_bytes(
        scene["cffi_pointer"],
        model_options["output_format"]
        )

    # Write to output
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    output_file.write(bytes_out)
