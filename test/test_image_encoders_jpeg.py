import pytest

from yoga.image.encoders import jpeg


class Test_open_jpeg(object):
    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/orientation/no-metadata.jpg",
            "test/images/orientation/1-rotation-0.jpg",
            "test/images/orientation/2-flip-horizontal.jpg",
            "test/images/orientation/3-rotation-180.jpg",
            "test/images/orientation/4-flip-vertical.jpg",
            "test/images/orientation/5-rotation-270-flip-horizontal.jpg",
            "test/images/orientation/6-rotation-270.jpg",
            "test/images/orientation/7-rotation-90-flip-horizontal.jpg",
            "test/images/orientation/8-rotation-90.jpg",
        ],
    )
    def test_jpeg_orientation(self, image_path):
        with open(image_path, "rb") as image_file:
            image = jpeg.open_jpeg(image_file)

            # Test image size
            assert image.width == 256
            assert image.height == 341

            # Check if the red square is at top-left corner
            r1, g1, b1 = image.getpixel((8, 8))
            assert r1 > 250 and g1 < 5 and b1 < 5  # ~red

            # Check if the green square is at top-right corner
            r2, g2, b2 = image.getpixel((255 - 8, 8))
            assert r2 < 5 and g2 > 250 and b2 < 5  # ~lime

            # Check if the blue square is at bottom-right corner
            r3, g3, b3 = image.getpixel((255 - 8, 340 - 8))
            assert r3 < 5 and g3 < 5 and b3 > 250  # ~blue
