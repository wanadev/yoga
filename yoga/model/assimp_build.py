import os

from cffi import FFI


_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
_ASSIMP_CPP = os.path.join(_ROOT, "assimp.cpp")
_ASSIMP_H = os.path.join(_ROOT, "assimp.h")


ffibuilder = FFI()
ffibuilder.set_source(
        "yoga.model._assimp",
        open(_ASSIMP_CPP, "r").read(),
        extra_objects=[
            os.path.join(_ROOT, "..", "..", "assimp", "build", "code", "libassimp.a"),  # noqa
            os.path.join(_ROOT, "..", "..", "assimp", "build", "contrib", "irrXML", "libIrrXML.a"), # noqa
            os.path.join(_ROOT, "..", "..", "assimp", "build", "contrib", "zlib", "libzlibstatic.a")  # noqa
            ],
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
