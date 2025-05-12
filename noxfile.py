# ruff: noqa: D100, D103
from __future__ import annotations

import os

import nox
from nox import options

PATH_TO_PROJECT = os.path.join(".", "ongaku")
EXAMPLES_PATH = os.path.join(".", "examples")
SCRIPT_PATHS = [
    PATH_TO_PROJECT,
    EXAMPLES_PATH,
    "noxfile.py",
    os.path.join(".", "tests"),
]

options.default_venv_backend = "uv"
options.sessions = [
    "format_fix",
    "import_fix",
    "pyright",
    "pytest",
    "docs",
]


def uv_sync(session: nox.Session, *groups: str) -> None:
    group_args: list[str] = []
    for group in groups:
        group_args.extend(["--group", group])

    session.run_install(
        "uv",
        "sync",
        "--locked",
        *group_args,
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session()
def format_fix(session: nox.Session) -> None:
    uv_sync(session, "format")
    session.run("python", "-m", "ruff", "format", *SCRIPT_PATHS)
    session.run("python", "-m", "ruff", "check", *SCRIPT_PATHS, "--fix")


@nox.session()
def import_fix(session: nox.Session) -> None:
    uv_sync(session, "format")
    session.run(
        "python",
        "-m",
        "ruff",
        "check",
        "--select",
        "I",
        *SCRIPT_PATHS,
        "--fix",
    )
    session.run("python", "-m", "ruff", "format", *SCRIPT_PATHS)


@nox.session()
def pyright(session: nox.Session) -> None:
    uv_sync(session)
    session.install(".[injection, speedups]")
    session.install("-U", "pyright")
    session.install("-Ur", "examples/examples_requirements.txt")
    session.run("pyright", PATH_TO_PROJECT, EXAMPLES_PATH)


@nox.session()
def pytest(session: nox.Session) -> None:
    uv_sync(session, "test")
    session.install("-U", ".[injection, dev]")
    session.run("pytest", "tests")


@nox.session()
def docs(session: nox.Session) -> None:
    uv_sync(session, "doc")
    session.install("-U", ".")
    session.run("python", "-m", "mkdocs", "build", "-q", "-s")


@nox.session()
def servedocs(session: nox.Session) -> None:
    uv_sync(session, "doc")
    session.install("-U", ".")
    session.run("python", "-m", "mkdocs", "serve")
