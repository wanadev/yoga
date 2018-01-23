from ._assimp import ffi

import io
import os.path
import yoga.image


def model_embed_images(images, images_bytes,
                       optimize_textures, root_path, image_options):
    image = images
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path).decode("utf-8")
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
        if optimize_textures:
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
