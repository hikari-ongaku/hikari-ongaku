from setuptools import setup, find_namespace_packages
import typing as t


name = "ongaku"


def long_description() -> str:
    with open("README.md") as fp:
        return fp.read()


def parse_requirements_file(path: str) -> t.List[str]:
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setup(
    name="hikari-ongaku",
    version="0.2.2",
    description="A command handler for hikari with a focus on type-safety and correctness.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="MPlaty",
    author_email="contact@mplaty.com",
    url="ongaku.mplaty.com",
    packages=find_namespace_packages(include=[name + "*"]),
    package_data={"arc": ["py.typed"]},
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements_file("requirements.txt"),
    extras_require={
        "docs": parse_requirements_file("doc_requirements.txt"),
    },
    python_requires=">=3.10.0,<3.13",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
