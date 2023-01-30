from importlib.metadata import version

__version__ = version("dls-logformatter")
del version

__all__ = ["__version__"]
