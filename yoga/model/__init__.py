from .assimp import (assimp_import_from_bytes, assimp_export_to_bytes)
from .options import (normalize_options)

from ._assimp import ffi # TODO Move image processing to helper
import os.path

def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    # TODO image_options = extract_image_options(options)

    # input_file -> string (path), bytes, file-like
    if not hasattr(input_file, "read"):
        input_file = open(input_file, "rb")
    if hasattr(input_file, "read"):
        input_file = input_file.read()

    # output_file -> string (path), file-like
    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    # Import the scene
    scene = assimp_import_from_bytes(input_file)

    # Embed images
    image = scene.images
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path)
        valid_image_path = image_path
        if not os.path.isfile(valid_image_path):
            # TODO How to specify root directory?
            valid_image_path = os.path.join("test/models", image_path)
            if not os.path.isfile(valid_image_path):
                raise RuntimeError("Cannot resolve image file %s" % image_path)

        image_bytes = open(valid_image_path, 'rb').read()

        # Optimizing images
        if not model_options["no_textures_optimization"]:
            # TODO
            print("Should optimize %s" % valid_image_path)

        # Convert to cffi
        image_bytes_c = ffi.new("char[%d]" % len(image_bytes), image_bytes)
        image.bytes_length = len(image_bytes)
        image.bytes = image_bytes_c
        image = image.next

    # Export the scene
    bytes_out = assimp_export_to_bytes(scene, model_options["output_format"])
    output_file.write(bytes_out)

    # TODO Don't forget to free memory in C++!
