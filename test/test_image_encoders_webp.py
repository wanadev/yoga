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


class Test_get_vp8x_info(object):
    def test_flag_icc(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_icc"] is False
        vp8x_info = webp.get_vp8x_info(
            b"\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_icc"] is True

    def test_flag_alpha(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_alpha"] is False
        vp8x_info = webp.get_vp8x_info(
            b"\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_alpha"] is True

    def test_flag_exif(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_exif"] is False
        vp8x_info = webp.get_vp8x_info(
            b"\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_exif"] is True

    def test_flag_xmp(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_xmp"] is False
        vp8x_info = webp.get_vp8x_info(
            b"\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_xmp"] is True

    def test_flag_animation(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_anim"] is False
        vp8x_info = webp.get_vp8x_info(
            b"\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert vp8x_info["has_anim"] is True

    def test_canvas_width(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\xAA\xBB\xCC\x00\x00\x00"
        )
        assert vp8x_info["canvas_width"] == 0xCCBBAA + 1

    def test_canvas_height(self):
        vp8x_info = webp.get_vp8x_info(
            b"\x00\x00\x00\x00\x00\x00\x00\xAA\xBB\xCC"
        )
        assert vp8x_info["canvas_height"] == 0xCCBBAA + 1


class Test_is_lossy_webp(object):
    def test_with_lossy_webp(object):
        image_bytes = open("test/images/alpha.lossy.webp", "rb").read()
        assert webp.is_lossy_webp(image_bytes) is True

    def test_with_lossless_webp(object):
        image_bytes = open("test/images/alpha.lossless.webp", "rb").read()
        assert webp.is_lossy_webp(image_bytes) is False

    def test_with_png(object):
        image_bytes = open("test/images/alpha.png", "rb").read()
        assert webp.is_lossy_webp(image_bytes) is False


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

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8 "]

    def test_unused_alpha(self):
        input_image = Image.open("test/images/unused-alpha.png")
        output_image_bytes = webp.optimize_lossy_webp(input_image, 0.90)
        riff = webp.get_riff_structure(output_image_bytes)

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8 "]

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

        # Checks there is only wanted chunks in the file
        for chunk in riff["chunks"]:
            assert chunk["type"] in ["VP8X", "VP8 ", "ALPH"]

        # Checks that the ALPH (alpha channel) chunk is present in the file
        alph_chunk_found = False
        for chunk in riff["chunks"]:
            if chunk["type"] == "ALPH":
                alph_chunk_found = True
        assert alph_chunk_found

    @pytest.mark.parametrize(
        "image_path",
        [
            "test/images/alpha.png",
            "test/images/threshold.png",
        ],
    )
    def test_alpha_vp8x_flags(self, image_path):
        input_image = Image.open(image_path)
        output_image_bytes = webp.optimize_lossy_webp(input_image, 0.90)
        riff = webp.get_riff_structure(output_image_bytes)

        vp8x_chunk = [c for c in riff["chunks"] if c["type"] == "VP8X"][0]
        vp8x_data = output_image_bytes[
            vp8x_chunk["data_offset"] : vp8x_chunk["data_offset"]
            + vp8x_chunk["size"]
        ]
        vp8x_info = webp.get_vp8x_info(vp8x_data)
        assert vp8x_info["has_alpha"] is True
        assert vp8x_info["has_icc"] is False
        assert vp8x_info["has_exif"] is False
        assert vp8x_info["has_xmp"] is False
        assert vp8x_info["has_anim"] is False

    def test_qualiy(self):
        input_image = Image.open("test/images/alpha.png")
        output_image_bytes_100 = webp.optimize_lossy_webp(input_image, 1.00)
        output_image_bytes_50 = webp.optimize_lossy_webp(input_image, 0.50)

        assert len(output_image_bytes_50) < len(output_image_bytes_100)
