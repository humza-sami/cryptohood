"""
CryptoHood: A Python client for the Robinhood Crypto API

This package provides a simple interface to interact with Robinhood's Crypto API,
allowing users to trade cryptocurrencies, fetch market data, and manage their accounts.
"""

from .client import CryptoHood
from .auth import CryptoHoodAuth
from .exceptions import (CryptoHoodAPIError, AuthenticationError, ValidationError, ClientError, ServerError, OrderError)

# Package metadata
__version__ = "0.1.0"
__author__ = "Humza Sami"
__license__ = "MIT"

# Export main classes and exceptions
__all__ = [
    "CryptoHood", "CryptoHoodAuth", "CryptoHoodAPIError", "AuthenticationError", "ValidationError", "ClientError", "ServerError",
    "OrderError"
]
