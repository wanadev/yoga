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
