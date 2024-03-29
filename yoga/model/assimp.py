"""
This module contains functions binded from the Assimp C++ API.
"""

from ._assimp import lib, ffi


def assimp_import_from_bytes(
    bytes_in, optimize_graph, optimize_meshes, fix_infacing_normals, verbose
):
    """Generates an abstract 3D scene from a model file's bytes.
    :param bytes_in: the input model's bytes
    :param optimize_graph: whether the graph scene should be optimized
    :param optimize_meshes: whether the meshes geometries should be optimized
    :param fix_infacing_normals: disable the assimp's "fix-infancing-normals"
                                 postprocess
    :param verbose: whether verbose is active
    :returns: An abstract scene dict
    :raises ValueError: Assimp was not able to import the model
    """

    flags = 0
    if optimize_graph:
        flags |= lib.FLAG_OPTIMIZE_GRAPH
    if optimize_meshes:
        flags |= lib.FLAG_OPTIMIZE_MESHES
    if fix_infacing_normals:
        flags |= lib.FLAG_FIX_INFACING_NORMALS

    scene = {
        "cffi_pointer": None,
        "cffi_gc": None,
    }
    scene["cffi_pointer"] = ffi.new("Scene*")
    scene["cffi_gc"] = ffi.gc(scene["cffi_pointer"], lib.assimp_free_scene)

    lib.assimp_import_from_bytes(
        bytes_in,
        len(bytes_in),
        flags,
        scene["cffi_pointer"],
        verbose,
    )

    if scene["cffi_pointer"].assimp_scene == ffi.NULL:
        raise ValueError(
            "Invalid model: Assimp was not able to import the model"
        )

    return scene


def assimp_export_to_bytes(scene_p, output_format):
    """Generates a glTF or a GLB file bytes from an abstract scene.
    :param scene_p: the abstract scene (a CFFI pointer)
    :param output_format: either "glb" or "gltf"
    :returns: the generated bytes making a glb or gltf file
    :rtype: bytes
    :raises ValueError: Assimp was not able to export the model
    """

    if output_format not in ("glb", "gltf"):
        raise ValueError(
            "Invalid output format: should be glb or gltf but is %s"
            % output_format
        )

    output_format_dict = dict(
        {
            "glb": lib.OUTPUT_FORMAT_GLB,
            "gltf": lib.OUTPUT_FORMAT_GLTF,
        }
    )

    bytes_out_p = ffi.new("char**")
    bytes_out_p_gc = ffi.gc(bytes_out_p, lib.assimp_free_bytes)

    length = lib.assimp_export_to_bytes(
        scene_p, output_format_dict[output_format], bytes_out_p
    )

    if length == 0:
        raise ValueError("Invalid model: Assimp was not able to export")

    bytes_out = ffi.cast("char*", bytes_out_p_gc[0])

    return ffi.unpack(bytes_out, length)
