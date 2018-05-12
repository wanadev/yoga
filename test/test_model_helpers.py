# coding: utf-8

import pytest

from yoga.model import helpers


class Test_model_helpers(object):

    def test_normalize_path(self):
        assert helpers.normalize_path(
            u"images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"./images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u".\\images\\texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"./images\\texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u".\\images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"../images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"..\\images\\texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"./images/subfolder/../texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"./images/sub1\\sub2/../../texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"./images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"/images/texture.png") == "images/texture.png"
        assert helpers.normalize_path(
            u"C:\\images\\texture.png") == "images/texture.png"

        assert helpers.normalize_path(
            u"somE_valid-caractères of files.png") == "some_valid-caracteres of files.png" # noqa

    def test_normalize_textures(self):
        textures = helpers.normalize_textures({
            "./images\\texture-1.png": True,
            "images/texture-2.png": True,
        })
        assert "images/texture-1.png" in textures
        assert "images/texture-2.png" in textures

        with pytest.raises(ValueError):
            helpers.normalize_textures({
                "images/texture.png": True,
                "./images/texture.png": True,
            })

    def test_find_valid_texture_path(self):
        textures = dict({
            "images/texture.png": True,
            "images/texture.jpg": True,
            "other_images/texture.jpg": True,
            "texture.gif": True,
        })

        assert helpers.find_valid_texture_path(
            "images/texture.png", textures) == "images/texture.png"
        assert helpers.find_valid_texture_path(
            "images/texture.jpg", textures) == "images/texture.jpg"
        assert helpers.find_valid_texture_path(
            "texture.png", textures) == "images/texture.png"

        assert helpers.find_valid_texture_path(
            "texture.jpg", textures) is None
        assert helpers.find_valid_texture_path(
            "non-existing.png", textures) is None
        assert helpers.find_valid_texture_path(
            "exture.png", textures) is None
