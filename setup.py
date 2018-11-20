#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class CustomBuildPy(build_py):

    def run(self):
        os.environ["CPPFLAGS"] = "--std=c++11"
        subprocess.call("cd assimp/ && mkdir -p build && cd build && \
                         cmake .. -DBUILD_SHARED_LIBS=OFF -DASSIMP_BUILD_ASSIMP_TOOLS=OFF -DASSIMP_BUILD_TESTS=OFF -DASSIMP_BUILD_ZLIB=ON && \
                         make", shell=True)
        build_py.run(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="yoga",
    version="0.10.1",
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
        "pillow>=4.0.0",
        "pyguetzli>=1.0.0",
        "unidecode>=1.0.0",
        "zopflipy>=1.0"
        ],

    entry_points={
        "console_scripts": [
            "yoga = yoga.__main__:main"
        ]},

    cffi_modules=["yoga/model/assimp_build.py:ffibuilder"],

    cmdclass={
        "build_py": CustomBuildPy,
        },
    )
