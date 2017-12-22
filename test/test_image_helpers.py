import pytest
from PIL import Image

from yoga.image import helpers


class Test_image_have_alpha(object):

    def test_jpeg_without_alpha(self):
        image = Image.open("test/images/image1.jpg")
        assert not helpers.image_have_alpha(image)

    def test_png_without_alpha(self):
        image = Image.open("test/images/unused-alpha.png")
        assert not helpers.image_have_alpha(image)

    def test_png_with_alpha(self):
        image = Image.open("test/images/alpha.png")
        assert helpers.image_have_alpha(image)

    def test_threshold(self):
        image = Image.open("test/images/threshold.png")
        assert helpers.image_have_alpha(image, 0xEF)
        assert not helpers.image_have_alpha(image, 0xE0)

    def test_indexed_png(self):
        image = Image.open("test/images/indexed.png")
        assert not helpers.image_have_alpha(image)

    def test_grayscale_png(self):
        image = Image.open("test/images/grayscale.png")
        assert not helpers.image_have_alpha(image)


class Test_gess_image_format(object):

    def test_jpeg_image(self):
        image_bytes = open("test/images/image1.jpg", "rb").read()
        assert helpers.guess_image_format(image_bytes) == "jpeg"

    def test_png_image(self):
        image_bytes = open("test/images/alpha.png", "rb").read()
        assert helpers.guess_image_format(image_bytes) == "png"

    def test_unsuported_image_format(self):
        image_bytes = open("test/images/alpha.svg", "rb").read()
        with pytest.raises(ValueError):
            helpers.guess_image_format(image_bytes)
