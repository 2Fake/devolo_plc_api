"""devolo PLC API"""
try:
    from setuptools_scm import get_version

    __version__ = get_version(fallback_version="0.0.0")
except ImportError:
    __version__ = "0.0.0"
