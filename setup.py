#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess
from distutils import ccompiler

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


def _find_msbuild(plat_spec="x64"):
    # https://github.com/python/cpython/blob/master/Lib/distutils/_msvccompiler.py
    import distutils._msvccompiler as msvc
    vc_env = msvc._get_vc_env(plat_spec)
    if "vsinstalldir" not in vc_env:
        raise Exception("Unable to find any Visual Studio installation")
    return os.path.join(vc_env["vsinstalldir"], "MSBuild", "Current", "Bin", "MSBuild.exe")  # noqa


class CustomBuildPy(build_py):

    def run(self):
        if not os.path.isdir("./assimp/build"):
            os.mkdir("./assimp/build")

        os.chdir("./assimp/build")

        if ccompiler.get_default_compiler() == "unix":
            os.environ["CPPFLAGS"] = "--std=c++11"
            subprocess.call([
                "cmake", "..",
                "-DBUILD_SHARED_LIBS=OFF",
                "-DASSIMP_BUILD_ASSIMP_TOOLS=OFF",
                "-DASSIMP_BUILD_TESTS=OFF",
                "-DASSIMP_BUILD_ZLIB=ON",
                ])
            subprocess.call(["make"])
        elif ccompiler.get_default_compiler() == "msvc":
            msbuild = _find_msbuild()
            subprocess.call([
                "cmake", "..",
                "-DBUILD_SHARED_LIBS=OFF",
                "-DASSIMP_BUILD_ASSIMP_TOOLS=OFF",
                "-DASSIMP_BUILD_TESTS=OFF",
                "-DASSIMP_BUILD_ZLIB=ON",
                "-DLIBRARY_SUFFIX=",
                ])
            subprocess.call([
                msbuild,
                "-p:Configuration=Release",
                "Assimp.sln"
                ])
        else:
            raise Exception("Unhandled platform")

        os.chdir("../..")

        build_py.run(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="yoga",
    version="0.11.1",
    description="Yummy Optimizer for Gorgeous Assets",
    url="https://github.com/wanadev/yoga",
    license="BSD-3-Clause",

    long_description=long_description,
    keywords="image jpeg png optimizer guetzli zopfli 3d model mesh assimp gltf glb converter",  # noqa

    author="Wanadev",
    author_email="contact@wanadev.fr",
    maintainer="Fabien LOISON, Alexis BREUST",

    packages=find_packages(),

    setup_requires=["cffi>=1.0.0"],
    install_requires=[
        "cffi>=1.0.0",
        "pillow>=6.2.2",
        "pyguetzli>=1.0.0",
        "unidecode>=1.0.0",
        "zopflipy>=1.0"
        ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "pytest",
            "Sphinx",
            "sphinx-rtd-theme",
        ]},

    entry_points={
        "console_scripts": [
            "yoga = yoga.__main__:main"
        ]},

    cffi_modules=["yoga/model/assimp_build.py:ffibuilder"],

    cmdclass={
        "build_py": CustomBuildPy,
        },
    )
