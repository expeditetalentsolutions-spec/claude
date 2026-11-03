"""AdSonar - search Meta's Ad Library through the official Graph API."""

from .client import AdLibraryClient, AdLibraryError

__version__ = "1.0.0"
__all__ = ["AdLibraryClient", "AdLibraryError", "__version__"]
