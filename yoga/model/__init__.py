from .assimp import (assimp_import_from_bytes, assimp_export_to_bytes)
from .options import (normalize_options, extract_image_options)

import io
import yoga.image

from ._assimp import ffi  # @todo Move image processing to helper
import os.path


def optimize(input_file, output_file, options={}):
    model_options = normalize_options(options)
    image_options = extract_image_options(options)

    root_path = "."
    if isinstance(input_file, basestring):
        root_path = os.path.dirname(os.path.abspath(input_file))
    if hasattr(input_file, "name"):
        root_path = os.path.dirname(os.path.abspath(input_file.name))

    # input_file -> string (path), bytes, file-like
    if not hasattr(input_file, "read"):
        input_file = open(input_file, "rb")
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
    image = scene.images
    images_bytes = dict()
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path)
        valid_image_path = image_path
        if not os.path.isfile(valid_image_path):
            valid_image_path = os.path.join(root_path, image_path)
            if not os.path.isfile(valid_image_path):
                raise RuntimeError(
                    "Cannot resolve image file %s, root_path is %s"
                    % (image_path, root_path)
                    )

        # Optimizing images
        image_io = io.BytesIO(open(valid_image_path, "rb").read())
        if not model_options["no_textures_optimization"]:
            print("Optimizing texture %s..." % valid_image_path)
            output_io = io.BytesIO()
            yoga.image.optimize(image_io, output_io, image_options)
            image_io = output_io

        image_io.seek(0)
        image_bytes = image_io.read()

        # Convert to cffi
        image_bytes_c = ffi.new("char[%d]" % len(image_bytes), image_bytes)
        image.bytes_length = len(image_bytes)
        image.bytes = image_bytes_c
        image = image.next

        # @note Save the bytes to a dictionnary so that the garbage collector
        # does not occur before exporting the scene a bit later
        images_bytes[valid_image_path] = image_bytes_c

    # Export the scene
    bytes_out = assimp_export_to_bytes(scene, model_options["output_format"])
    output_file.write(bytes_out)

    # @fixme Don't forget to free memory in C++!
