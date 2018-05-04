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

    return None


def find_valid_texture_path(path, textures):
    # In textures, all paths are supposed to be relative

    tested_path = path
    if tested_path in textures:
        return tested_path

    tested_path = os.path.basename(path)
    if tested_path in textures:
        return tested_path

    path = path.replace("\\", "/")

    tested_path = path
    if tested_path in textures:
        return tested_path

    tested_path = os.path.basename(path)
    if tested_path in textures:
        return tested_path

    return None


def model_embed_images(
        images,
        images_bytes,
        optimize_textures,
        fallback_texture,
        root_path,
        image_options,
        textures
        ):
    optimized_images = {}

    image = images
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path).decode("utf-8")

        # If textures exists, we don't look for files on the file system
        valid_image_path = None
        if textures is not None:
            valid_image_path = find_valid_texture_path(image_path, textures)
        else:
            valid_image_path = find_valid_path(image_path, root_path)
            if valid_image_path is not None:
                valid_image_path = os.path.abspath(valid_image_path)

        # Unable to find a valid image path
        if valid_image_path is None:
            if fallback_texture is not None:
                print("Warning: Cannot resolve file %s, using the fallback texture instead." % image_path) # noqa
                valid_image_path = None
            else:
                raise RuntimeError("Cannot resolve file %s" % image_path)

        # If valid_image_path have already been seen, do not reoptimize...
        if valid_image_path in optimized_images:
            optimized_image = optimized_images[valid_image_path]
            image.bytes_length = optimized_image.bytes_length
            image.bytes = optimized_image.bytes
            image.id = optimized_image.id
            image = image.next
            continue

        # Get the bytes indeed
        image_io = None
        if valid_image_path is None:
            image_io = fallback_texture
        elif textures is not None:
            image_io = textures[valid_image_path]
        else:
            image_io = io.BytesIO(open(valid_image_path, "rb").read())

        # Optimizing the texture if requested
        if optimize_textures:
            if valid_image_path is not None:
                print("Optimizing texture %s..." % valid_image_path)
            else:
                print("Optimizing fallback texture...")
            output_io = io.BytesIO()
            yoga.image.optimize(image_io, output_io, image_options)
            image_io = output_io

        image_io.seek(0)
        image_bytes = image_io.read()

        # Convert to cffi
        image_bytes_c = ffi.new("char[%d]" % len(image_bytes), image_bytes)
        image.bytes_length = len(image_bytes)
        image.bytes = image_bytes_c
        image.id = len(optimized_images)

        optimized_images[valid_image_path] = image
        image = image.next

        # @note Save the bytes to a dictionnary so that the garbage collector
        # does not occur before exporting the scene a bit later
        images_bytes[valid_image_path] = image_bytes_c
