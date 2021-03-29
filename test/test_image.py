import io
import os

import pytest
from PIL import Image

import yoga.image


_MAGIC_PNG = b"\x89PNG\r\n"
_MAGIC_JPEG = b"\xFF\xD8\xFF\xE0"


class Test_optimize(object):
    @pytest.mark.parametrize(
        "input_",
        [
            "test/images/alpha.png",
            open("test/images/alpha.png", "rb"),
            io.BytesIO(open("test/images/alpha.png", "rb").read()),
        ],
    )
    def test_input_file(self, input_):
        output = io.BytesIO()
        yoga.image.optimize(input_, output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    def test_output_path(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output1.png")
        yoga.image.optimize("test/images/alpha.png", output_path)
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_PNG)

    def test_output_file(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output2.png")
        output = open(output_path, "wb")
        yoga.image.optimize("test/images/alpha.png", output)
        output.close()
        output = open(output_path, "rb")
        assert output.read().startswith(_MAGIC_PNG)

    def test_output_bytesio(self):
        output = io.BytesIO()
        yoga.image.optimize("test/images/alpha.png", output)
        output.seek(0)
        assert output.read().startswith(_MAGIC_PNG)

    @pytest.mark.parametrize(
        "image_path,magic",
        [
            ("test/images/image1.jpg", _MAGIC_JPEG),
            ("test/images/unused-alpha.png", _MAGIC_PNG),
        ],
    )
    def test_option_output_format_default(self, image_path, magic):
        output = io.BytesIO()
        yoga.image.optimize(image_path, output)
        output.seek(0)
        assert output.read().startswith(magic)

    @pytest.mark.parametrize(
        "image_path,format_,magic",
        [
            # fmt: off
            ("test/images/image1.jpg",       "orig", _MAGIC_JPEG),
            ("test/images/unused-alpha.png", "orig", _MAGIC_PNG),
            ("test/images/alpha.png",        "auto", _MAGIC_PNG),
            ("test/images/unused-alpha.png", "auto", _MAGIC_JPEG),
            ("test/images/image1.jpg",       "auto", _MAGIC_JPEG),
            ("test/images/image1.jpg",       "jpeg", _MAGIC_JPEG),
            ("test/images/unused-alpha.png", "jpeg", _MAGIC_JPEG),
            ("test/images/image1.jpg",       "png",  _MAGIC_PNG),
            ("test/images/unused-alpha.png", "png",  _MAGIC_PNG),
            # fmt: on
        ],
    )
    def test_option_output_format(self, image_path, format_, magic):
        output = io.BytesIO()
        yoga.image.optimize(image_path, output, {"output_format": format_})
        output.seek(0)
        assert output.read().startswith(magic)

    def test_option_output_format_orig_with_unsuported_output_format(self):
        output = io.BytesIO()
        with pytest.raises(ValueError):
            yoga.image.optimize(
                "test/images/image.gif", output, {"output_format": "orig"}
            )

    @pytest.mark.parametrize(
        "image_path,options,output_image_size",
        [
            # fmt: off
            # IMAGE                       OPTIONS               OUT IMG SIZE
            # orig
            ["test/images/image1.jpg",    {"resize": "orig"},   (256, 256)],
            # size < image
            ["test/images/image1.jpg",    {"resize": 128},      (128, 128)],
            ["test/images/image1.jpg",    {"resize": 96},       (96, 96)],
            # size > image
            ["test/images/image1.jpg",    {"resize": 512},      (256, 256)],
            # width, height
            ["test/images/image1.jpg",    {"resize": "96x200"}, (96, 96)],
            ["test/images/landscape.png", {"resize": [64, 64]}, (64, 32)],
            ["test/images/landscape.png", {"resize": [96, 64]}, (96, 48)],
            ["test/images/landscape.png", {"resize": [96, 32]}, (64, 32)],
            ["test/images/portrait.png",  {"resize": [64, 64]}, (32, 64)],
            ["test/images/portrait.png",  {"resize": [64, 96]}, (48, 96)],
            ["test/images/portrait.png",  {"resize": [32, 96]}, (32, 64)],
            # fmt: on
        ],
    )
    def test_option_resize(self, image_path, options, output_image_size):
        output = io.BytesIO()
        yoga.image.optimize(image_path, output, options)
        output.seek(0)
        image = Image.open(output)
        assert image.width == output_image_size[0]
        assert image.height == output_image_size[1]

    def test_jpeg_quality(self):
        output1 = io.BytesIO()
        yoga.image.optimize(
            "test/images/image1.jpg", output1, {"jpeg_quality": 1.00}
        )
        output1.seek(0)

        output2 = io.BytesIO()
        yoga.image.optimize(
            "test/images/image1.jpg", output2, {"jpeg_quality": 0.50}
        )
        output2.seek(0)

        assert len(output2.read()) < len(output1.read())

    @pytest.mark.skip(reason="Requires output_format=auto")
    def test_opacity_threshold(self):
        raise NotImplementedError()  # TODO

    # TODO test wrong image / fuzzy inputs
