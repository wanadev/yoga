from .assimp import (assimp_import_from_bytes, assimp_export_to_bytes)
from .options import (normalize_options, extract_image_options)
from .helpers import model_embed_images

import os.path


def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    # Open file if possible
    if not hasattr(input_file, "read"):
        input_file = open(input_file, "rb")

    root_path = "."
    if hasattr(input_file, "name"):
        root_path = os.path.dirname(os.path.abspath(input_file.name))

    # input_file -> string (path), bytes, file-like
    if hasattr(input_file, "read"):
        input_file = input_file.read()

    # output_file -> string (path), file-like
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    # Import the scene
    scene = assimp_import_from_bytes(
        input_file,
        not model_options["no_graph_optimization"],
        not model_options["no_meshes_optimization"]
        )

    # Embed images
    # @note We save the bytes to a dictionnary so that the garbage collector
    # does not occur before exporting the scene a bit later
    images_bytes = dict()
    model_embed_images(
        scene["cffi_pointer"].images,
        images_bytes,
        not model_options["no_textures_optimization"],
        root_path,
        image_options
        )

    # Export the scene
    bytes_out = assimp_export_to_bytes(
        scene["cffi_pointer"],
        model_options["output_format"]
        )
    output_file.write(bytes_out)
