import os
from distutils import ccompiler

from cffi import FFI


_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
_ASSIMP_CPP = os.path.join(_ROOT, "assimp.cpp")
_ASSIMP_H = os.path.join(_ROOT, "assimp.h")


_LIB_ASSIMP = None
_LIB_ZLIB = None
_EXTRA_LIBS = []
_EXTRA_ARGS = []

if ccompiler.get_default_compiler() == "unix":
    # Default libs path for Unix systems
    _LIB_ASSIMP = os.path.join(
        _ROOT, "..", "..", "assimp", "build", "lib", "libassimp.a"
    )
    _LIB_ZLIB = os.path.join(
        _ROOT,
        "..",
        "..",
        "assimp",
        "build",
        "contrib",
        "zlib",
        "libzlibstatic.a",
    )
    _EXTRA_ARGS = ["--std=c++11"]
elif ccompiler.get_default_compiler() == "msvc":
    # Default libs path for Windows
    _LIB_ASSIMP = os.path.join(
        _ROOT, "..", "..", "assimp", "build", "lib", "Release", "assimp.lib"
    )
    _LIB_ZLIB = os.path.join(
        _ROOT,
        "..",
        "..",
        "assimp",
        "build",
        "contrib",
        "zlib",
        "Release",
        "zlibstatic.lib",
    )
    _EXTRA_LIBS.append("Advapi32.lib")

# Allow to override path through env vars
if "YOGA_BUILD_LIB_ASSIMP" in os.environ:
    _LIB_ASSIMP = os.environ["YOGA_BUILD_LIB_ASSIMP"]
if "YOGA_BUILD_LIB_ZLIB" in os.environ:
    _LIB_ZLIB = os.environ["YOGA_BUILD_LIB_ZLIB"]

if not _LIB_ASSIMP:
    raise Exception(
        "Please provide the path to the assimp library using the YOGA_BUILD_LIB_ASSIMP environment variable"
    )
if not _LIB_ZLIB:
    raise Exception(
        "Please provide the path to the zlib library using the YOGA_BUILD_LIB_ZLIB environment variable"
    )


ffibuilder = FFI()
ffibuilder.set_source(
    "yoga.model._assimp",
    open(_ASSIMP_CPP, "r").read(),
    extra_objects=[_LIB_ASSIMP, _LIB_ZLIB] + _EXTRA_LIBS,
    include_dirs=[
        _ROOT,
        os.path.join(_ROOT, "..", "..", "assimp", "include"),
        os.path.join(_ROOT, "..", "..", "assimp", "build", "include"),
    ],
    source_extension=".cpp",
    extra_compile_args=_EXTRA_ARGS,
)
ffibuilder.cdef(open(_ASSIMP_H, "r").read())


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
