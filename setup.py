# ruff: noqa: D100, D103
from setuptools import setup, find_namespace_packages
import typing as t
import types
import os
import re


name = "ongaku"


def long_description() -> str:
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path: str) -> t.List[str]:
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


def parse_meta() -> types.SimpleNamespace:
    with open(os.path.join(name, "internal", "about.py")) as fp:
        code = fp.read()

    token_pattern = re.compile(
        r"^__(?P<key>\w+)?__\s*:?.*=\s*(?P<quote>(?:'{3}|\"{3}|'|\"))(?P<value>.*?)(?P=quote)",
        re.M,
    )

    groups = {}

    for match in token_pattern.finditer(code):
        group = match.groupdict()
        groups[group["key"]] = group["value"]

    return types.SimpleNamespace(**groups)


meta = parse_meta()

setup(
    name="hikari-ongaku",
    version=meta.version,
    description="A voice library, for hikari.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author=meta.author,
    author_email=meta.author_email,
    url="https://github.com/MPlatypus/hikari-ongaku",
    packages=find_namespace_packages(include=[name + "*"]),
    package_data={"ongaku": ["py.typed"]},
    license=meta.license,
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements_file("requirements.txt"),
    extras_require={
        "docs": parse_requirements_file("doc_requirements.txt"),
        "dev": parse_requirements_file("dev_requirements.txt"),
    },
    python_requires=">=3.11.0, <3.13",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
)
