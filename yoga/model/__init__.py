from .assimp import (assimp_import_from_bytes, assimp_export_to_bytes)
from .options import (normalize_options)


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

    # Import the bytes
    scene = assimp_import_from_bytes(input_file)
    bytes_out = assimp_export_to_bytes(scene, model_options["output_format"])
    output_file.write(bytes_out)

    # TODO Don't forget to free memory in C++!
