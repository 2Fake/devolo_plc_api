import setuptools

from devolo_plc_api import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="devolo_plc_api",
    version=__version__,
    author="Markus Bong, Guido Schmitz",
    author_email="m.bong@famabo.de, guido.schmitz@fedaix.de",
    description="devolo PLC devices in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2Fake/devolo_plc_api",
    packages=setuptools.find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx>=0.14,<0.17",
        "protobuf",
        "zeroconf>=0.27.0",
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "asynctest;python_version<'3.8'",
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "pytest-mock",
    ],
    python_requires='>=3.7',
)
