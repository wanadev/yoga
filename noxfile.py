import nox


PYTHON_FILES = [
    "yoga",
    "test",
    "setup.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--line-length=79", "--check", *PYTHON_FILES)


@nox.session(python=["2.7", "3.7", "3.8", "3.9"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "test")


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install(".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
