import pytest
from PIL import Image

from yoga.image import helpers


class Test_image_have_alpha(object):
    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/image1.jpg",
            "test/images/unused-alpha.png",
            "test/images/indexed.png",
            "test/images/grayscale.png",
        ],
    )
    def test_image_without_alpha(self, image_path):
        image = Image.open(image_path)
        assert not helpers.image_have_alpha(image)

    def test_image_with_alpha(self):
        image = Image.open("test/images/alpha.png")
        assert helpers.image_have_alpha(image)

    @pytest.mark.parametrize(
        "image_path, threshold, is_alpha",
        [
            ("test/images/threshold.png", 0xEF, True),
            ("test/images/threshold.png", 0xE0, False),
        ],
    )
    def test_alpha_threshold(self, image_path, threshold, is_alpha):
        image = Image.open("test/images/threshold.png")
        if is_alpha:
            assert helpers.image_have_alpha(image, threshold)
        else:
            assert not helpers.image_have_alpha(image, threshold)


class Test_little_endian_unint32_bytes_to_python_int(object):
    def test_uint32_value(self):
        assert (
            helpers.little_endian_unint32_bytes_to_python_int(
                b"\x78\x56\x34\x12"
            )
            == 305419896
        )


class Test_get_riff_structure(object):
    @pytest.fixture
    def webp_image(self):
        return open("test/images/alpha.lossless.metadata.webp", "rb").read()

    def test_riff_structure(object, webp_image):
        riff = helpers.get_riff_structure(webp_image)
        assert riff["formtype"] == "WEBP"
        assert riff["size"] == 11868
        assert len(riff["chunks"]) == 5
        assert riff["chunks"][0]["id"] == "VP8X"
        assert riff["chunks"][1]["id"] == "ICCP"
        assert riff["chunks"][2]["id"] == "VP8L"
        assert riff["chunks"][3]["id"] == "EXIF"
        assert riff["chunks"][4]["id"] == "XMP "


class Test_guess_image_format(object):
    @pytest.mark.parametrize(
        "image_path, expected_format",
        [
            ("test/images/image1.jpg", "jpeg"),
            ("test/images/alpha.png", "png"),
            ("test/images/alpha.lossy.webp", "webp"),
            ("test/images/alpha.lossless.webp", "webpl"),
            ("test/images/alpha.lossless.metadata.webp", "webpl"),
        ],
    )
    def test_supported_image_format(self, image_path, expected_format):
        image_bytes = open(image_path, "rb").read()
        assert helpers.guess_image_format(image_bytes) == expected_format

    def test_unsuported_image_format(self):
        image_bytes = open("test/images/alpha.svg", "rb").read()
        with pytest.raises(ValueError):
            helpers.guess_image_format(image_bytes)

    def test_unsuported_animated_webp(self):
        image_bytes = open("test/images/animated.webp", "rb").read()
        with pytest.raises(ValueError):
            helpers.guess_image_format(image_bytes)
