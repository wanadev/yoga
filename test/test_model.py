import io
import os
import json

import pytest

import yoga.model


_MAGIC_GLB = b"glTF"


class Test_optimize(object):

    def test_input_file(self):
        # str (path)
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

        # file
        input_ = open("test/models/model.fbx", "rb")
        output = io.BytesIO()
        yoga.model.optimize(input_, output)
        input_.close()
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

        # ByteIO
        input_ = io.BytesIO(open("test/models/model.fbx", "rb").read())
        output = io.BytesIO()
        yoga.model.optimize(input_, output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)


    def test_input_file_format(self):
        # FBX
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

        # DAE
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.dae", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_output_file(self, tmpdir):
        # str (path)
        output_path = os.path.join(str(tmpdir), "output1.glb")
        yoga.model.optimize("test/models/model.fbx", output_path)
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_GLB)

        # file
        output_path = os.path.join(str(tmpdir), "output2.glb")
        output = open(output_path, "wb")
        yoga.model.optimize("test/models/model.fbx", output)
        output.close()
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_GLB)

        # ByteIO
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

    def test_option_output_format(self):
        # GLB
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output, {
            "output_format": "glb"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_GLB)

        # glTF
        output = io.BytesIO()
        yoga.model.optimize("test/models/model.fbx", output, {
            "output_format": "gltf"
            })
        output.seek(0)
        assert json.load(output)["asset"]["version"] == 2

    # TODO Tests for no_graph_optimization and such
