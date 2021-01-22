import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "yoga", "test", "noxfile.py")


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "-v", "test")


@nox.session
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install(".")
    session.run("sphinx-build", "-M", "html", "doc", "build")
