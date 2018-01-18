from .assimp import (assimp_import_from_bytes)
from .options import (normalize_options, extract_image_options)


def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    assimp_import_from_bytes("glb", bytes([0, 0, 0, 0])) # @fixme

    # TODO input_file -> string (path), bytes, file-like
    # TODO output_file -> string (path), file-like
    # raise NotImplementedError()  # TODO
