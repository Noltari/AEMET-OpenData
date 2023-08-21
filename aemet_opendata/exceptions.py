"""AEMET OpenData API exceptions."""
from __future__ import annotations


class AemetError(Exception):
    """Base class for AEMET OpenData errors."""


class AuthError(AemetError):
    """Exception raised when API denies access."""


class TooManyRequests(AemetError):
    """Exception raised when max API requests are exceeded."""
