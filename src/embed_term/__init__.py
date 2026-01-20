"""
embed-term: A module to embed a terminal-like input in Python applications.
"""

from .term import EmbedTerminal
from . import formats
from . import readchar

__version__ = "0.1.0"
__author__ = "Glenn Sutherland"
__all__ = ["EmbedTerminal", "formats", "readchar"]
