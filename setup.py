from setuptools import setup, find_packages

def long_description() -> str:
    with open("README.md") as fp:
        return fp.read()

setup(
    name='hikari-ongaku',
    version='0.1.1',
    author='MPlaty',
    author_email='mplatypus54@gmail.com',
    description='A Music handler for hikari!',
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.11',
    requires=["hikari", "aiohttp"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
    ]
)
