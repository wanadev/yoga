import io
import os

import pytest
from PIL import Image

import yoga.image


_MAGIC_PNG = b"\x89PNG\r\n"
_MAGIC_JPEG = b"\xFF\xD8\xFF\xE0"


class Test_optimize(object):

    def test_input_file(self):
        # str (path)
        output = io.BytesIO()
        yoga.image.optimize("test/images/alpha.png", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

        # file
        input_ = open("test/images/alpha.png", "rb")
        output = io.BytesIO()
        yoga.image.optimize(input_, output)
        input_.close()
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

        # ByteIO
        input_ = io.BytesIO(open("test/images/alpha.png", "rb").read())
        output = io.BytesIO()
        yoga.image.optimize(input_, output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    def test_output_file(self, tmpdir):
        # str (path)
        output_path = os.path.join(str(tmpdir), "output1.png")
        yoga.image.optimize("test/images/alpha.png", output_path)
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_PNG)

        # file
        output_path = os.path.join(str(tmpdir), "output2.png")
        output = open(output_path, "wb")
        yoga.image.optimize("test/images/alpha.png", output)
        output.close()
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_PNG)

        # ByteIO
        output = io.BytesIO()
        yoga.image.optimize("test/images/alpha.png", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    def test_option_output_format_default(self):
        # JPEG
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_JPEG)

        # PNG
        output = io.BytesIO()
        yoga.image.optimize("test/images/unused-alpha.png", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    def test_option_output_format_orig(self):
        # JPEG
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "output_format": "orig"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_JPEG)

        # PNG
        output = io.BytesIO()
        yoga.image.optimize("test/images/unused-alpha.png", output, {
            "output_format": "orig"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

        # Other
        output = io.BytesIO()
        with pytest.raises(ValueError):
            yoga.image.optimize("test/images/image.gif", output, {
                "output_format": "orig"
                })

    @pytest.mark.skip(reason="will be implemented later")
    def test_option_output_format_auto(self):
        raise NotImplementedError()  # TODO
        # jpeg -> jpeg
        # png -> jpeg
        # png -> png
        # jpeg -> png

    def test_option_output_format_jpeg(self):
        # JPEG
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "output_format": "jpeg"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_JPEG)

        # PNG
        output = io.BytesIO()
        yoga.image.optimize("test/images/unused-alpha.png", output, {
            "output_format": "jpeg"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_JPEG)

    def test_option_output_format_png(self):
        # JPEG
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "output_format": "png"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

        # PNG
        output = io.BytesIO()
        yoga.image.optimize("test/images/unused-alpha.png", output, {
            "output_format": "png"
            })
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    def test_option_resize(self):
        # orig
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "resize": "orig"
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 256
        assert image.height == 256

        # size < image
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "resize": 128
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 128
        assert image.height == 128

        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "resize": "96"
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 96
        assert image.height == 96

        # size > image
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "resize": 512
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 256
        assert image.height == 256

        # width, height
        output = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output, {
            "resize": "96x200"
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 96
        assert image.height == 96

        output = io.BytesIO()
        yoga.image.optimize("test/images/landscape.png", output, {
            "resize": [64, 64]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 64
        assert image.height == 32

        output = io.BytesIO()
        yoga.image.optimize("test/images/landscape.png", output, {
            "resize": [96, 64]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 96
        assert image.height == 48

        output = io.BytesIO()
        yoga.image.optimize("test/images/landscape.png", output, {
            "resize": [96, 32]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 64
        assert image.height == 32

        output = io.BytesIO()
        yoga.image.optimize("test/images/portrait.png", output, {
            "resize": [64, 64]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 32
        assert image.height == 64

        output = io.BytesIO()
        yoga.image.optimize("test/images/portrait.png", output, {
            "resize": [64, 96]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 48
        assert image.height == 96

        output = io.BytesIO()
        yoga.image.optimize("test/images/portrait.png", output, {
            "resize": [32, 96]
            })
        output.seek(0)
        image = Image.open(output)
        assert image.width == 32
        assert image.height == 64

    def test_jpeg_quality(self):
        output1 = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output1, {
            "jpeg_quality": 1.00
            })
        output1.seek(0)

        output2 = io.BytesIO()
        yoga.image.optimize("test/images/image1.jpg", output2, {
            "jpeg_quality": 0.50
            })
        output2.seek(0)

        assert len(output2.read()) < len(output1.read())

    @pytest.mark.skip(reason="Requires output_format=auto")
    def test_opacity_threshold(self):
        raise NotImplementedError()  # TODO

    # TODO test wrong image / fuzzy inputs
