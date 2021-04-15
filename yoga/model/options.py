DEFAULT_OPTIONS = {
    "output_format": "glb",  # glb|gltf
    "fallback_texture": None,
    "no_graph_optimization": False,
    "no_meshes_optimization": False,
    "no_textures_optimization": False,
    "no_fix_infacing_normals": False,
}


def normalize_options(options=None):
    if not options:
        return dict(DEFAULT_OPTIONS)

    result = dict(DEFAULT_OPTIONS)

    # "GLB" -> "glb" (lower case)
    if "output_format" in options:
        value = options["output_format"].lower()

        if value not in ("gltf", "glb"):
            raise ValueError("Invalid value for 'output_format': '%s'" % value)

        result["output_format"] = value

    # Fallback texture
    if "fallback_texture" in options:
        fallback_texture_file = options["fallback_texture"]

        if fallback_texture_file:
            if not hasattr(fallback_texture_file, "read"):
                fallback_texture_file = open(fallback_texture_file, "rb")

            result["fallback_texture"] = fallback_texture_file

    # Flags
    for key in (
        "no_graph_optimization",
        "no_meshes_optimization",
        "no_textures_optimization",
        "no_fix_infacing_normals",
    ):
        if key in options:
            result[key] = bool(options[key])

    return result


def extract_image_options(options=None):
    if not options:
        return None

    result = dict()

    for key in options:
        if key.startswith("image_"):
            result[key[6:]] = options[key]

    return result
