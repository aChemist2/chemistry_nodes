"""Top-level package for chemistry_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """TheWierdChemist"""
__email__ = "you@gmail.com"
__version__ = "0.0.1"

from .src.chemistry_nodes.danbooru import BooruTags

NODE_CLASS_MAPPINGS = {
    "Booru Tags from ID": BooruTags,
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "Booru Tags from ID": "Booru Tags from ID",
}

WEB_DIRECTORY = "./web"

print("--> chemistry_nodes loaded")
