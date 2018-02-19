from .options import DEFAULT_OPTIONS


def add_model_cli_options(parser):
    parser.add_argument(
            "--output-format",
            help="format of the output model (default: %s)" % DEFAULT_OPTIONS["output_format"], # noqa
            metavar="{glb,gltf}",
            choices=["glb", "gltf"],
            default=DEFAULT_OPTIONS["output_format"]
            )
    parser.add_argument(
            "--no-graph-optimization",
            help="disable empty graph nodes merging",
            default=DEFAULT_OPTIONS["no_graph_optimization"],
            action="store_true"
            )
    parser.add_argument(
            "--no-meshes-optimization",
            help="disable meshes optimization",
            default=DEFAULT_OPTIONS["no_meshes_optimization"],
            action="store_true"
            )
    parser.add_argument(
            "--no-textures-optimization",
            help="disable textures optimization using yoga image",
            default=DEFAULT_OPTIONS["no_textures_optimization"],
            action="store_true"
            )
