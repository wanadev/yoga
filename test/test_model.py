import io
import os
import json

import pytest
import yoga.model


_MAGIC_GLB = b"glTF"


class Test_optimize(object):

    def test_input_file_path(self):
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_input_file(self):
        input_ = open("test/models/model.fbx", "rb")
        output = io.BytesIO()
        yoga.model.optimize(input_, output)
        input_.close()
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_input_bytesio(self):
        with pytest.raises(RuntimeError):
            input_ = io.BytesIO(open("test/models/model.fbx", "rb").read())
            output = io.BytesIO()
            yoga.model.optimize(input_, output)

    @pytest.mark.parametrize("model_path", [
        "test/models/model.fbx",
        "test/models/model.dae",
        ])
    def test_input_file_format(self, model_path):
        output = io.BytesIO()
        yoga.model.optimize(model_path, output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_textures_empty_dictionary(self):
        with pytest.raises(RuntimeError):
            input_ = open("test/models/model.fbx", "rb")
            output = io.BytesIO()
            yoga.model.optimize(input_, output, {}, {})

    def test_textures_dictionary(self):
        input_ = open("test/models/model.fbx", "rb")
        output = io.BytesIO()
        yoga.model.optimize(input_, output, {}, {
            "diffuse.jpg": open("test/models/diffuse.jpg", "rb")
        })
        input_.close()
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_output_file_path(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output1.glb")
        yoga.model.optimize("test/models/model.fbx", output_path)
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_GLB)

    def test_output_file(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output2.glb")
        output = open(output_path, "wb")
        yoga.model.optimize("test/models/model.fbx", output)
        output.close()
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_GLB)

    def test_output_bytesio(self):
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_glb_output_format(self):
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output, {
            "output_format": "glb"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    @pytest.mark.skip("Format not supported yet")
    def test_gltf_output_format(self):
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output, {
            "output_format": "gltf"
            })
        output.seek(0)
        assert json.load(output)["asset"]["version"] == "2.0"

    # TODO Tests for no_graph_optimization and such
