import pytest

from yoga.image import options


class Test_normalize_options(object):
    def test_no_parameter_returns_default_options(self):
        opt = options.normalize_options()

        assert opt is not options.DEFAULT_OPTIONS

        for k, v in options.DEFAULT_OPTIONS.items():
            assert k in opt
            assert opt[k] == v

    @pytest.mark.parametrize(
        "option_name,input_,output",
        [
            # output_format
            ("output_format", "orig", "orig"),
            ("output_format", "auto", "auto"),
            ("output_format", "jpeg", "jpeg"),
            ("output_format", "png", "png"),
            ("output_format", "AuTo", "auto"),
            ("output_format", "jpg", "jpeg"),
            ("output_format", "JPG", "jpeg"),
            # resize
            ("resize", "orig", "orig"),
            ("resize", "OrIg", "orig"),
            # jpeg_quality
            ("jpeg_quality", 0.42, 0.42),
            ("jpeg_quality", 42, 0.42),
            ("jpeg_quality", "0.42", 0.42),
            ("jpeg_quality", ".42", 0.42),
            ("jpeg_quality", "42", 0.42),
            ("jpeg_quality", b"0.42", 0.42),
            ("jpeg_quality", b".42", 0.42),
            ("jpeg_quality", b"42", 0.42),
            ("jpeg_quality", u"0.42", 0.42),
            ("jpeg_quality", u".42", 0.42),
            ("jpeg_quality", u"42", 0.42),
            # webp_quality
            ("webp_quality", 0.42, 0.42),
            ("webp_quality", 42, 0.42),
            ("webp_quality", "0.42", 0.42),
            ("webp_quality", ".42", 0.42),
            ("webp_quality", "42", 0.42),
            ("webp_quality", b"0.42", 0.42),
            ("webp_quality", b".42", 0.42),
            ("webp_quality", b"42", 0.42),
            ("webp_quality", u"0.42", 0.42),
            ("webp_quality", u".42", 0.42),
            ("webp_quality", u"42", 0.42),
            # opacity_threshold
            ("opacity_threshold", 128, 128),
            ("opacity_threshold", 0.5, 128),
            ("opacity_threshold", "128", 128),
            ("opacity_threshold", "0.5", 128),
            ("opacity_threshold", ".5", 128),
            ("opacity_threshold", 255, 255),
            ("opacity_threshold", "255", 255),
            ("opacity_threshold", 300, 255),
            ("opacity_threshold", "300", 255),
            ("opacity_threshold", b"255", 255),
            ("opacity_threshold", u"255", 255),
        ],
    )
    def test_options(self, option_name, input_, output):
        opt = options.normalize_options({option_name: input_})
        assert opt[option_name] == output

    @pytest.mark.parametrize(
        "input_,output",
        [
            (100, [100, 100]),
            ("101", [101, 101]),
            ("100x200", [100, 200]),
            ("100X200", [100, 200]),
            ("100 200", [100, 200]),
            ("100:200", [100, 200]),
            ("100,200", [100, 200]),
            ("100;200", [100, 200]),
            (u"100x200", [100, 200]),
            (b"100x200", [100, 200]),
            ([100, 200], [100, 200]),
        ],
    )
    def test_numeric_resize_option(self, input_, output):
        opt = options.normalize_options({"resize": input_})
        assert opt["resize"][0] == output[0]
        assert opt["resize"][1] == output[1]

    def test_invalid_resize_option(self):
        with pytest.raises(ValueError):
            options.normalize_options({"resize": "foobar"})
