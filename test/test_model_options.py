import io
import pytest

from yoga.model import options


class Test_normalize_options(object):

    def test_no_parameter_returns_default_options(self):
        opt = options.normalize_options()

        assert opt is not options.DEFAULT_OPTIONS

        for k, v in options.DEFAULT_OPTIONS.items():
            assert k in opt
            assert opt[k] == v

    def test_output_format_option(self):
        opt = options.normalize_options({"output_format": "glb"})
        assert opt["output_format"] == "glb"

        opt = options.normalize_options({"output_format": "gltf"})
        assert opt["output_format"] == "gltf"

        opt = options.normalize_options({"output_format": "glTF"})
        assert opt["output_format"] == "gltf"

        with pytest.raises(ValueError):
            options.normalize_options({"output_format": "foobar"})

    def test_fallback_image(self):
        opt = options.normalize_options({})
        assert opt["fallback_texture"] is None

        opt = options.normalize_options({"fallback_texture": None})
        assert opt["fallback_texture"] is None

        opt = options.normalize_options({"fallback_texture": "test/models/diffuse.jpg"})
        assert opt["fallback_texture"] is not None

        fallback_texture = io.BytesIO()
        opt = options.normalize_options({"fallback_texture": fallback_texture})
        assert opt["fallback_texture"] is not None

        with pytest.raises(IOError):
            opt = options.normalize_options({"fallback_texture": "non-existant.jpg"})

    def test_no_graph_optimization(self):
        opt = options.normalize_options({"no_graph_optimization": True})
        assert opt["no_graph_optimization"] is True

        opt = options.normalize_options({"no_graph_optimization": False})
        assert opt["no_graph_optimization"] is False

        opt = options.normalize_options({"no_graph_optimization": ""})
        assert opt["no_graph_optimization"] is False

        opt = options.normalize_options({"no_graph_optimization": "foobar"})
        assert opt["no_graph_optimization"] is True

    def test_no_meshes_optimization(self):
        opt = options.normalize_options({"no_meshes_optimization": True})
        assert opt["no_meshes_optimization"] is True

        opt = options.normalize_options({"no_meshes_optimization": False})
        assert opt["no_meshes_optimization"] is False

        opt = options.normalize_options({"no_meshes_optimization": ""})
        assert opt["no_meshes_optimization"] is False

        opt = options.normalize_options({"no_meshes_optimization": "foobar"})
        assert opt["no_meshes_optimization"] is True

    def test_no_textures_optimization(self):
        opt = options.normalize_options({"no_textures_optimization": True})
        assert opt["no_textures_optimization"] is True

        opt = options.normalize_options({"no_textures_optimization": False})
        assert opt["no_textures_optimization"] is False

        opt = options.normalize_options({"no_textures_optimization": ""})
        assert opt["no_textures_optimization"] is False

        opt = options.normalize_options({"no_textures_optimization": "foobar"})
        assert opt["no_textures_optimization"] is True
