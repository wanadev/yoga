from PIL import Image
import pytest

from yoga.image.encoders import png


class Test_big_endian_unint32_bytes_to_python_int(object):
    def test_uint32_value(self):
        assert (
            png.big_endian_uint32_bytes_to_python_int(b"\xaa\xbb\xcc\xdd")
            == 0xAABBCCDD
        )


class Test_python_int_to_big_endian_uint32_bytes(object):
    def test_python_int_value(self):
        assert (
            png.python_int_to_big_endian_uint32_bytes(0xAABBCCDD)
            == b"\xaa\xbb\xcc\xdd"
        )


class Test_get_png_structure(object):
    @pytest.fixture
    def png_image(self):
        return open("test/images/alpha.png", "rb").read()

    def test_png_structure(self, png_image):
        png_structure = png.get_png_structure(png_image)
        assert png_structure["size"] == 2832
        assert len(png_structure["chunks"]) == 6
        assert png_structure["chunks"][0]["type"] == "IHDR"
        assert png_structure["chunks"][1]["type"] == "sBIT"
        assert png_structure["chunks"][2]["type"] == "pHYs"
        assert png_structure["chunks"][3]["type"] == "tEXt"
        assert png_structure["chunks"][4]["type"] == "IDAT"
        assert png_structure["chunks"][5]["type"] == "IEND"


class Test_get_IHDR_info(object):
    def test_width(self):
        ihdr_info = png.get_IHDR_info(
            b"\x00\x00\xc0\xfe\x00\x00\x00\xee\x08\x00\x00\x00\x00"
            # |width          |height         |bit|clr|cmp|flt|interlace
        )
        assert ihdr_info["width"] == 49406

    def test_height(self):
        ihdr_info = png.get_IHDR_info(
            b"\x00\x00\x00\xff\x00\x00\x00\xee\x08\x00\x00\x00\x00"
            # |width          |height         |bit|clr|cmp|flt|interlace
        )
        assert ihdr_info["height"] == 238

    def test_bit_depth(self):
        ihdr_info = png.get_IHDR_info(
            b"\x00\x00\x00\xff\x00\x00\x00\xee\x08\x00\x00\x00\x00"
            # |width          |height         |bit|clr|cmp|flt|interlace
        )
        assert ihdr_info["bit_depth"] == 8

    @pytest.mark.parametrize(
        "ihdr, id_,name",
        [
            # fmt: off
            # .|width          |height         |bit|clr|cmp|flt|interlace
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x00\x00\x00\x00", 0, "grayscale"),
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x02\x00\x00\x00", 2, "truecolour"),
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x03\x00\x00\x00", 3, "indexed-colour"),
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x04\x00\x00\x00", 4, "grayscale-alpha"),
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x06\x00\x00\x00", 6, "truecolour-alpha"),
            # fmt: on
        ],
    )
    def test_colour_type(self, ihdr, id_, name):
        ihdr_info = png.get_IHDR_info(ihdr)
        assert ihdr_info["colour_type"] == id_
        assert ihdr_info["colour_type_str"] == name

    def test_compression_method(self):
        ihdr_info = png.get_IHDR_info(
            b"\x00\x00\x00\xff\x00\x00\x00\xee\x08\x00\x00\x00\x00"
            # |width          |height         |bit|clr|cmp|flt|interlace
        )
        assert ihdr_info["compression_method"] == 0
        assert ihdr_info["compression_method_str"] == "deflate"

    def test_filter_method(self):
        ihdr_info = png.get_IHDR_info(
            b"\x00\x00\x00\xff\x00\x00\x00\xee\x08\x00\x00\x00\x00"
            # |width          |height         |bit|clr|cmp|flt|interlace
        )
        assert ihdr_info["filter_method"] == 0
        assert ihdr_info["filter_method_str"] == "adaptative"

    @pytest.mark.parametrize(
        "ihdr, id_,name",
        [
            # fmt: off
            # .|width          |height         |bit|clr|cmp|flt|interlace
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x00\x00\x00\x00", 0, "no-interlace"),
            (b"\x00\x00\x00\xFF\x00\x00\x00\xEE\x08\x00\x00\x00\x01", 1, "Adam7"),
            # fmt: on
        ],
    )
    def test_interlace_method(self, ihdr, id_, name):
        ihdr_info = png.get_IHDR_info(ihdr)
        assert ihdr_info["interlace_method"] == id_
        assert ihdr_info["interlace_method_str"] == name


class Test_assemble_png_from_chunks(object):
    def test_assemble_png_from_chunks(self):
        chunks = [
            {
                "type": "IHDR",
                "data": b"\x00\x00\x00\x78\x00\x00\x00\x78\x08\x06\x00\x00\x00",
            },
            {
                "type": "tEXt",
                "data": b"Foo\0Bar",
            },
            {
                "type": "IDAT",
                "data": b"\xaa\xbb",
            },
            {
                "type": "IEND",
                "data": b"",
            },
        ]

        expected_png = b"\x89PNG\r\n\x1a\n"
        # IHDR
        expected_png += b"\x00\x00\x00\x0d"  # length
        expected_png += b"IHDR"  # type
        expected_png += b"\x00\x00\x00\x78\x00\x00\x00\x78\x08\x06\x00\x00\x00"
        expected_png += b"\x39\x64\x36\xd2"  # CRC
        # tEXt
        expected_png += b"\x00\x00\x00\x07"  # length
        expected_png += b"tEXt"  # type
        expected_png += b"Foo\0Bar"  # data
        expected_png += b"\xc8\x97\x2e\x75"  # CRC
        # IDAT
        expected_png += b"\x00\x00\x00\x02"  # length
        expected_png += b"IDAT"  # type
        expected_png += b"\xaa\xbb"  # data
        expected_png += b"\x74\xa0\x83\xdd"  # CRC
        # IEND
        expected_png += b"\x00\x00\x00\x00"  # length
        expected_png += b"IEND"  # type
        expected_png += b"\xae\x42\x60\x82"  # CRC

        assert png.assemble_png_from_chunks(chunks) == expected_png


class Test_is_png(object):
    def test_png_file(self):
        with open("test/images/alpha.png", "rb") as image_file:
            image_data = image_file.read()

        assert png.is_png(image_data) is True

    def test_jpeg_file(self):
        with open("test/images/image1.jpg", "rb") as image_file:
            image_data = image_file.read()

        assert png.is_png(image_data) is False


class Test_optimize_png(object):
    @pytest.mark.parametrize(
        "filename",
        [
            "test/images/edgecases/calibre-gui.png",
            "test/images/edgecases/keepassxc.png",
            "test/images/edgecases/vlc.png",
        ],
    )
    def test_output_png_never_larger_than_input_png(self, filename):
        with open(filename, "rb") as image_file:
            image_data = image_file.read()
            image_file.seek(0)
            image = Image.open(image_file)

            output = png.optimize_png(image, image_data)

        assert len(output) <= len(image_data)
