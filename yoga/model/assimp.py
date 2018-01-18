"""
This module contains functions binded from the Assimp C++ API.
"""


from ._assimp import lib, ffi


def assimp_import_from_bytes(output_format, bytes_in):
    """
    @fixme doc
    """

    scene = lib.assimp_import_from_bytes(
            0xFF,  # @fixme How to pass optimization flags?
            bytes_in,
            len(bytes_in)
            )

    if scene.assimp_scene == ffi.NULL:
        raise ValueError("Invalid model: Assimp was not able to import the model")  # noqa

    print("Model was imported")


    # OUTPUTTING...

    output_format_dict = dict({
            "glb": lib.OUTPUT_FORMAT_GLB,
            "gltf": lib.OUTPUT_FORMAT_GLTF
        })
    print(output_format_dict[output_format])
