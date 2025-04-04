import nox


PYTHON_FILES = [
    "yoga",
    "test",
    "setup.py",
    "noxfile.py",
]

PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black", "codespell")
    session.run("flake8", *PYTHON_FILES)
    session.run(
        "black",
        "--line-length=79",
        "--check",
        "--diff",
        "--color",
        *PYTHON_FILES,
    )
    session.run(
        "codespell",
        "-L",
        "ans,alph,ccompiler",
        "doc/",
        "scripts/",
        "test/",
        "winbuild/",
        "yoga/",
        "noxfile.py",
        "README.rst",
        "setup.py",
    )


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "test")


@nox.session(reuse_venv=False)
def test_build_wheel(session):
    session.install("build")
    session.run("python", "-m", "build")


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install(".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
