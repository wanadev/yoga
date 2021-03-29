# coding: utf-8

import pytest

from yoga.model import helpers


class Test_model_helpers(object):
    def test_normalize_path(self):
        assert (
            helpers.normalize_path(u"images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"./images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u".\\images\\texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"./images\\texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u".\\images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"../images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"..\\images\\texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"./images/subfolder/../texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"./images/sub1\\sub2/../../texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"./images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"/images/texture.png")
            == "images/texture.png"
        )
        assert (
            helpers.normalize_path(u"C:\\images\\texture.png")
            == "images/texture.png"
        )

        assert (
            helpers.normalize_path(u"somE_valid-caractères of files.png")
            == "some_valid-caracteres of files.png"
        )

    def test_normalize_paths(self):
        paths = helpers.normalize_paths(
            {
                "./images\\texture-1.png": True,
                "images/texture-2.png": True,
            }
        )
        assert "images/texture-1.png" in paths
        assert "images/texture-2.png" in paths

        with pytest.raises(ValueError):
            helpers.normalize_paths(
                {
                    "images/texture.png": True,
                    "./images/texture.png": True,
                }
            )

    def test_find_valid_path(self):
        paths = dict(
            {
                "images/texture.png": True,
                "images/texture.jpg": True,
                "other_images/texture.jpg": True,
                "texture.gif": True,
            }
        )

        assert (
            helpers.find_valid_path("images/texture.png", paths)
            == "images/texture.png"
        )
        assert (
            helpers.find_valid_path("images/texture.jpg", paths)
            == "images/texture.jpg"
        )
        assert (
            helpers.find_valid_path("texture.png", paths)
            == "images/texture.png"
        )

        assert helpers.find_valid_path("texture.jpg", paths) is None
        assert helpers.find_valid_path("non-existing.png", paths) is None
        assert helpers.find_valid_path("exture.png", paths) is None
