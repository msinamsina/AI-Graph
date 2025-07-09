"""AI-Graph: A framework for building and managing AI workflows."""

# using importlib.metadata
import importlib.metadata

__version__ = importlib.metadata.version(__name__)

__all__ = ["__version__"]
