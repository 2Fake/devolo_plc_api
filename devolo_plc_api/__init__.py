"""devolo PLC API"""
try:
    from setuptools_scm import get_version

    __version__ = get_version()
except ImportError:
    __version__ = "0.0.0"
