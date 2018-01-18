import io

from .assimp import (assimp_import_from_bytes)
from .options import (normalize_options, extract_image_options)


def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    if not hasattr(input_file, "read"):
        input_file = open(input_file, "rb")
    if hasattr(input_file, "read"):
        input_file = input_file.read()

    if not hasattr(output_file, "write"):
        output_file = open(output_file, "wb")

    assimp_import_from_bytes("glb", input_file)    # @fixme

    # TODO input_file -> string (path), bytes, file-like
    # TODO output_file -> string (path), file-like
    # raise NotImplementedError()  # TODO

    output_file.write(b"glTF")
