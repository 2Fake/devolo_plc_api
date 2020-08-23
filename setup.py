import setuptools

from devolo_home_control_api import __version__


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
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aiohttp",
        "protobuf",
        "zeroconf"
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-mock"
    ],
    python_requires='>=3.6',
)
