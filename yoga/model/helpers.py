from ._assimp import ffi

import io
import os.path
import yoga.image


def find_valid_path(path, root_path):
    tested_path = path
    if os.path.isfile(tested_path):
        return tested_path

    tested_path = os.path.join(root_path, path)
    if os.path.isfile(tested_path):
        return tested_path

    tested_path = os.path.join(root_path, os.path.basename(path))
    if os.path.isfile(tested_path):
        return tested_path

    # Still not able to find it, it might be a Windows path,
    # while this program is executed on Linux.
    # So paths like "..\\image.png" are seen as entire filename,
    # we try some trick.

    path = path.replace("\\", "/")

    tested_path = path
    if os.path.isfile(tested_path):
        return tested_path

    tested_path = os.path.join(root_path, path)
    if os.path.isfile(tested_path):
        return tested_path

    tested_path = os.path.join(root_path, os.path.basename(path))
    if os.path.isfile(tested_path):
        return tested_path

    raise RuntimeError(
        "Cannot resolve file %s, root_path is %s"
        % (path, root_path)
        )


def model_embed_images(images, images_bytes,
                       optimize_textures, root_path, image_options):
    image = images
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path).decode("utf-8")
        valid_image_path = find_valid_path(image_path, root_path)

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
