"""AEMET OpenData API exceptions."""

from __future__ import annotations


class AemetError(Exception):
    """Base class for AEMET OpenData errors."""


class AemetTimeout(AemetError):
    """Exception raised when API times out."""


class AuthError(AemetError):
    """Exception raised when API denies access."""


class ApiError(AemetError):
    """Exception raised when data is not provided by API."""


class StationNotFound(AemetError):
    """Exception raised when there are no stations close to provided coordinates."""


class TooManyRequests(AemetError):
    """Exception raised when max API requests are exceeded."""


class TownNotFound(AemetError):
    """Exception raised when there are no towns close to provided coordinates."""
