import pytest

from yoga.image import options


class Test_normalize_options(object):

    def test_no_parameter_returns_default_options(self):
        opt = options.normalize_options()

        assert opt is not options.DEFAULT_OPTIONS

        for k, v in options.DEFAULT_OPTIONS.items():
            assert k in opt
            assert opt[k] == v

    def test_output_format_option(self):
        opt = options.normalize_options({"output_format": "orig"})
        assert opt["output_format"] == "orig"

        opt = options.normalize_options({"output_format": "auto"})
        assert opt["output_format"] == "auto"

        opt = options.normalize_options({"output_format": "jpeg"})
        assert opt["output_format"] == "jpeg"

        opt = options.normalize_options({"output_format": "png"})
        assert opt["output_format"] == "png"

        opt = options.normalize_options({"output_format": "AuTo"})
        assert opt["output_format"] == "auto"

        opt = options.normalize_options({"output_format": "jpg"})
        assert opt["output_format"] == "jpeg"

        with pytest.raises(ValueError):
            options.normalize_options({"output_format": "foobar"})

    def test_resize_option(self):
        opt = options.normalize_options({"resize": "orig"})
        assert opt["resize"] == "orig"

        opt = options.normalize_options({"resize": "OrIg"})
        assert opt["resize"] == "orig"

        opt = options.normalize_options({"resize": 100})
        assert opt["resize"][0] == 100
        assert opt["resize"][1] == 100

        opt = options.normalize_options({"resize": "101"})
        assert opt["resize"][0] == 101
        assert opt["resize"][1] == 101

        for s in ["100x200", "100X200", "100 200", "100:200",
                  "100,200", "100;200", u"100x200", b"100x200",
                  [100, 200]]:
            opt = options.normalize_options({"resize": s})
            assert opt["resize"][0] == 100
            assert opt["resize"][1] == 200

        with pytest.raises(ValueError):
            options.normalize_options({"resize": "foobar"})

    def test_jpeg_quality_option(self):
        for q in [0.42, 42, "0.42", "42", ".42", b"42", u"42"]:
            opt = options.normalize_options({"jpeg_quality": q})
            assert opt["jpeg_quality"] == 0.42

        for q in [1, 100, "1", "1.00", "100", 110, "110", "110.42"]:
            opt = options.normalize_options({"jpeg_quality": q})
            assert opt["jpeg_quality"] == 1

    def test_opacity_threshold_option(self):
        for th in [128, 0.5, "128", "0.5", ".5"]:
            opt = options.normalize_options({"opacity_threshold": th})
            assert opt["opacity_threshold"] == 128

        for th in [255, "255", 300, "300", b"255", u"255"]:
            opt = options.normalize_options({"opacity_threshold": th})
            assert opt["opacity_threshold"] == 255

        opt = options.normalize_options({"opacity_threshold": 1})
        assert opt["opacity_threshold"] == 1
