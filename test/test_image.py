import io
import os

import pytest
from PIL import Image

import yoga.image
from yoga.image.encoders.jpeg import is_jpeg
from yoga.image.encoders.png import is_png
from yoga.image.encoders.webp import is_lossy_webp
from yoga.image.encoders.webp_lossless import is_lossless_webp


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
        assert is_png(output.read())

    def test_output_path(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output1.png")
        yoga.image.optimize("test/images/alpha.png", output_path)
        output = open(output_path, "rb")
        assert is_png(output.read())

    def test_output_file(self, tmpdir):
        output_path = os.path.join(str(tmpdir), "output2.png")
        output = open(output_path, "wb")
        yoga.image.optimize("test/images/alpha.png", output)
        output.close()
        output = open(output_path, "rb")
        assert is_png(output.read())

    def test_output_bytesio(self):
        output = io.BytesIO()
        yoga.image.optimize("test/images/alpha.png", output)
        output.seek(0)
        assert is_png(output.read())

    @pytest.mark.parametrize(
        "image_path,format_checker",
        [
            ("test/images/image1.jpg", is_jpeg),
            ("test/images/unused-alpha.png", is_png),
            ("test/images/alpha.lossy.webp", is_lossy_webp),
            ("test/images/alpha.lossless.webp", is_lossless_webp),
        ],
    )
    def test_option_output_format_default(self, image_path, format_checker):
        output = io.BytesIO()
        yoga.image.optimize(image_path, output)
        output.seek(0)
        assert format_checker(output.read())

    @pytest.mark.parametrize(
        "image_path,format_,format_checker",
        [
            # fmt: off
            ("test/images/image1.jpg",          "orig",  is_jpeg),
            ("test/images/unused-alpha.png",    "orig",  is_png),
            ("test/images/alpha.png",           "auto",  is_png),
            ("test/images/unused-alpha.png",    "auto",  is_jpeg),
            ("test/images/image1.jpg",          "auto",  is_jpeg),
            ("test/images/image1.jpg",          "jpeg",  is_jpeg),
            ("test/images/unused-alpha.png",    "jpeg",  is_jpeg),
            ("test/images/image1.jpg",          "png",   is_png),
            ("test/images/unused-alpha.png",    "png",   is_png),
            ("test/images/alpha.lossy.webp",    "webp",  is_lossy_webp),
            ("test/images/alpha.lossy.webp",    "orig",  is_lossy_webp),
            ("test/images/alpha.lossless.webp", "webpl", is_lossless_webp),
            ("test/images/alpha.lossless.webp", "orig",  is_lossless_webp),
            # fmt: on
        ],
    )
    def test_option_output_format(self, image_path, format_, format_checker):
        output = io.BytesIO()
        yoga.image.optimize(image_path, output, {"output_format": format_})
        output.seek(0)
        assert format_checker(output.read())

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

    def test_webp_quality(self):
        output1 = io.BytesIO()
        yoga.image.optimize(
            "test/images/alpha.lossy.webp", output1, {"webp_quality": 1.00}
        )
        output1.seek(0)

        output2 = io.BytesIO()
        yoga.image.optimize(
            "test/images/alpha.lossy.webp", output2, {"webp_quality": 0.50}
        )
        output2.seek(0)

        assert len(output2.read()) < len(output1.read())

    @pytest.mark.skip(reason="Requires output_format=auto")
    def test_opacity_threshold(self):
        raise NotImplementedError()  # TODO

    # TODO test wrong image / fuzzy inputs
