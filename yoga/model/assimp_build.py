import os
from distutils import ccompiler

from cffi import FFI


_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
_ASSIMP_CPP = os.path.join(_ROOT, "assimp.cpp")
_ASSIMP_H = os.path.join(_ROOT, "assimp.h")


_LIB_ASSIMP = None
_LIB_IRRXML = None
_LIB_ZLIB = None

if ccompiler.get_default_compiler() == "unix":
    # Default libs path for Unix systems
    _LIB_ASSIMP = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "libassimp.a")  # noqa
    _LIB_IRRXML = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "libIrrXML.a")  # noqa
    _LIB_ZLIB = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "libzlibstatic.a")  # noqa
elif ccompiler.get_default_compiler() == "msvc":
    # Default libs path for Windows
    _LIB_ASSIMP = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "Release", "assimp.lib")  # noqa
    _LIB_IRRXML = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "Release", "IrrXML.lib")  # noqa
    _LIB_ZLIB = os.path.join(_ROOT, "..", "..", "assimp", "build", "lib", "Release", "zlibstatic.lib")  # noqa

# Allow to override path through env vars
if "YOGA_BUILD_LIB_ASSIMP" in os.environ:
    _LIB_ASSIMP = os.environ["YOGA_BUILD_LIB_ASSIMP"]
if "YOGA_BUILD_LIB_IRRXML" in os.environ:
    _LIB_IRRXML = os.environ["YOGA_BUILD_LIB_IRRXML"]
if "YOGA_BUILD_LIB_ZLIB" in os.environ:
    _LIB_ZLIB = os.environ["YOGA_BUILD_LIB_ZLIB"]

if not _LIB_ASSIMP:
    raise Exception("Please provide the path to the assimp library using the YOGA_BUILD_LIB_ASSIMP environment variable")  # noqa
if not _LIB_IRRXML:
    raise Exception("Please provide the path to the IrrXML library using the YOGA_BUILD_LIB_IRRXML environment variable")  # noqa
if not _LIB_ZLIB:
    raise Exception("Please provide the path to the zlib library using the YOGA_BUILD_LIB_ZLIB environment variable")  # noqa


ffibuilder = FFI()
ffibuilder.set_source(
        "yoga.model._assimp",
        open(_ASSIMP_CPP, "r").read(),
        extra_objects=[_LIB_ASSIMP, _LIB_IRRXML, _LIB_ZLIB],
        include_dirs=[
            _ROOT,
            os.path.join(_ROOT, "..", "..", "assimp", "include"),
            os.path.join(_ROOT, "..", "..", "assimp", "build", "include")
            ],
        source_extension=".cpp"
        )
ffibuilder.cdef(open(_ASSIMP_H, "r").read())


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
