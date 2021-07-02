from PIL import Image
import pytest

from yoga.image.encoders import webp
from yoga.image.encoders import webp_lossless


class Test_is_lossless_webp(object):
    def test_with_lossy_webp(self):
        image_bytes = open("test/images/alpha.lossy.webp", "rb").read()
        assert webp_lossless.is_lossless_webp(image_bytes) is False

    def test_with_lossless_webp(self):
        image_bytes = open("test/images/alpha.lossless.webp", "rb").read()
        assert webp_lossless.is_lossless_webp(image_bytes) is True

    def test_with_png(self):
        image_bytes = open("test/images/alpha.png", "rb").read()
        assert webp_lossless.is_lossless_webp(image_bytes) is False


class Test_encode_lossless_webp(object):
    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/image1.jpg",
            "test/images/indexed.png",
            "test/images/grayscale.png",
        ],
    )
    def test_no_alpha(self, image_path):
        input_image = Image.open(image_path)
        output_image_bytes = webp_lossless.optimize_lossless_webp(input_image)
        riff = webp.get_riff_structure(output_image_bytes)

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8L"]

    def test_unused_alpha(self):
        input_image = Image.open("test/images/unused-alpha.png")
        output_image_bytes = webp_lossless.optimize_lossless_webp(input_image)
        riff = webp.get_riff_structure(output_image_bytes)

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8L"]

    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/alpha.png",
            "test/images/threshold.png",
        ],
    )
    def test_alpha(self, image_path):
        input_image = Image.open(image_path)
        output_image_bytes = webp_lossless.optimize_lossless_webp(input_image)
        riff = webp.get_riff_structure(output_image_bytes)

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8L"]
