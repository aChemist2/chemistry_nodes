"""Top-level package for chemistry_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """TheWierdChemist"""
__email__ = "you@gmail.com"
__version__ = "0.0.1"

from .src.chemistry_nodes.nodes import NODE_CLASS_MAPPINGS
from .src.chemistry_nodes.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
