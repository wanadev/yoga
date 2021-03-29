from ._assimp import ffi

import io
import sys
import os.path

import unidecode

import yoga.image


def normalize_path(path):
    # Expects a unicode path, returns a ascii one.
    # Paths are normalized to a standard linux relative path,
    # without a point, and lowercase.
    # That is to say /images\subfolder/..\texture.png -> images/texture.png
    # It does not correspond to an effective path,
    # as the backslashes on linux are wrongly seen as separators.
    # This function is meant to give a standard output.

    path = unidecode.unidecode(path)
    split_path = path.replace("\\", "/").split("/")[::-1]
    normalized_path = []
    ignored_folders = 0

    for name in split_path:
        if name == "" or name == "." or name[-1:] == ":":
            continue
        elif name == "..":
            ignored_folders += 1
        elif ignored_folders > 0:
            ignored_folders -= 1
        else:
            normalized_path.append(name)

    return "/".join(normalized_path[::-1]).lower()


def normalize_paths(paths):
    if paths is None:
        return None

    # Normalizes all the paths in the texture dict.
    normalized_paths = dict()
    for path in paths:
        normalized_path = normalize_path(path)
        if normalized_path in normalized_paths:
            raise ValueError(
                "Multiple paths are resolved to the same path %s."
                % normalized_path
            )
        normalized_paths[normalized_path] = paths[path]

    return normalized_paths


def find_valid_path(path, paths):
    if paths is None:
        return None

    # The path and the paths are supposed to have
    # already been normalized.

    split_path = path.split("/")[::-1]
    split_paths = map(lambda p: p.split("/")[::-1], paths.keys())

    for i, name in enumerate(split_path):
        split_paths = list(
            filter(lambda sp: len(sp) > i and sp[i] == name, split_paths)
        )

        if len(split_paths) == 0:
            break
        elif len(split_paths) == 1:
            return "/".join(split_paths[0][::-1])

    return None


def extract_files_dictionary(root_path):
    if root_path is None:
        return None

    if sys.version_info.major == 2 and type(root_path) is str:
        root_path = root_path.decode("utf-8")

    # Recursive walk of root_path files
    files = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(root_path)
        for f in filenames
    ]
    return normalize_paths(dict(zip(files, files)))


def model_embed_images(
    images,
    images_bytes,
    optimize_textures,
    fallback_texture,
    root_path,
    image_options,
    textures,
    quiet,
):
    optimized_textures = {}
    normalized_textures = normalize_paths(textures)
    files = extract_files_dictionary(root_path)

    image = images
    while image:
        if image.bytes_length > 0:
            continue

        image_path = ffi.string(image.path).decode("utf-8")

        # If textures exists, we don't look for files on the file system
        normalized_image_path = normalize_path(image_path)
        if normalized_textures is not None:
            valid_image_path = find_valid_path(
                normalized_image_path, normalized_textures
            )
        else:
            valid_image_path = find_valid_path(normalized_image_path, files)

        # Unable to find a valid image path
        if valid_image_path is None:
            if fallback_texture is not None:
                valid_image_path = None
                if not quiet:
                    print(
                        "Warning: Cannot resolve %s, using the fallback texture instead."  # noqa: E501
                        % normalized_image_path
                    )
            else:
                raise ValueError("Cannot resolve %s" % normalized_image_path)

        # If valid_image_path have already been seen, do not reoptimize...
        if valid_image_path in optimized_textures:
            optimized_texture = optimized_textures[valid_image_path]
            image.bytes_length = optimized_texture.bytes_length
            image.bytes = optimized_texture.bytes
            image.id = optimized_texture.id
            image = image.next
            continue

        # Get the bytes indeed
        image_io = None
        if valid_image_path is None:
            image_io = fallback_texture
        elif textures is not None:
            image_io = textures[valid_image_path]
        else:
            image_io = io.BytesIO(open(files[valid_image_path], "rb").read())

        # Optimizing the texture if requested
        if optimize_textures:
            if not quiet:
                if valid_image_path is not None:
                    print("Optimizing texture %s..." % normalized_image_path)
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
        image.id = len(optimized_textures)

        optimized_textures[valid_image_path] = image
        image = image.next

        # @note Save the bytes to a dictionnary so that the garbage collector
        # does not occur before exporting the scene a bit later
        images_bytes[valid_image_path] = image_bytes_c
