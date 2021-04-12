from PIL import Image
import pytest

from yoga.image.encoders import webp


class Test_little_endian_unint32_bytes_to_python_int(object):
    def test_uint32_value(self):
        assert (
            webp.little_endian_unint32_bytes_to_python_int(b"\x78\x56\x34\x12")
            == 305419896
        )


class Test_get_riff_structure(object):
    @pytest.fixture
    def webp_image(self):
        return open("test/images/alpha.lossless.metadata.webp", "rb").read()

    def test_riff_structure(object, webp_image):
        riff = webp.get_riff_structure(webp_image)
        assert riff["formtype"] == "WEBP"
        assert riff["size"] == 11868
        assert len(riff["chunks"]) == 5
        assert riff["chunks"][0]["type"] == "VP8X"
        assert riff["chunks"][1]["type"] == "ICCP"
        assert riff["chunks"][2]["type"] == "VP8L"
        assert riff["chunks"][3]["type"] == "EXIF"
        assert riff["chunks"][4]["type"] == "XMP "


class Test_encode_lossy_webp(object):
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
        output_image_bytes = webp.optimize_lossy_webp(input_image, 0.90)
        riff = webp.get_riff_structure(output_image_bytes)

        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8X", "VP8 "]

    def test_unused_alpha(self):
        input_image = Image.open("test/images/unused-alpha.png")
        output_image_bytes = webp.optimize_lossy_webp(input_image, 0.90)
        riff = webp.get_riff_structure(output_image_bytes)

        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8X", "VP8 "]

    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/alpha.png",
            "test/images/threshold.png",
        ],
    )
    def test_alpha(self, image_path):
        input_image = Image.open(image_path)
        output_image_bytes = webp.optimize_lossy_webp(input_image, 0.90)
        riff = webp.get_riff_structure(output_image_bytes)

        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8X", "VP8 ", "ALPH"]

    def test_qualiy(self):
        input_image = Image.open("test/images/alpha.png")
        output_image_bytes_100 = webp.optimize_lossy_webp(input_image, 1.00)
        output_image_bytes_50 = webp.optimize_lossy_webp(input_image, 0.50)

        assert len(output_image_bytes_50) < len(output_image_bytes_100)
