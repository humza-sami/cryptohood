from typing import Dict, Optional, List


class CryptoHoodAPIError(Exception):
    """Base exception class for CryptoHood API errors."""

    def __init__(self, message: str):
        super().__init__(message)


class AuthenticationError(CryptoHoodAPIError):
    """Raised when there's an authentication-related error."""

    def __init__(self, message: str):
        super().__init__(f"Authentication failed: {message}")


class ValidationError(CryptoHoodAPIError):
    """
    Raised when the API returns a validation error (HTTP 400).
    Contains details about which fields failed validation.
    """

    def __init__(self, error_response: Dict):
        self.type = error_response.get('type', 'validation_error')
        self.errors = error_response.get('errors', [])

        # Create a formatted error message
        error_details = []
        for error in self.errors:
            attr = error.get('attr', 'unknown_field')
            detail = error.get('detail', 'no detail provided')
            error_details.append(f"{attr}: {detail}")

        message = "Validation failed:\n" + "\n".join(error_details)
        super().__init__(message)

    def get_field_errors(self) -> Dict[str, str]:
        """
        Returns a dictionary of field names and their error messages.
        """
        return {error.get('attr'): error.get('detail') for error in self.errors if error.get('attr')}


class ClientError(CryptoHoodAPIError):
    """
    Raised for client-side errors (HTTP 4XX, except 400).
    """

    def __init__(self, error_response: Dict):
        self.type = error_response.get('type', 'client_error')
        self.errors = error_response.get('errors', [])
        self.status_code = error_response.get('status_code', 400)

        error_message = "\n".join(error.get('detail', 'Unknown error') for error in self.errors)

        message = f"Client error (HTTP {self.status_code}): {error_message}"
        super().__init__(message)


class ServerError(CryptoHoodAPIError):
    """
    Raised for server-side errors (HTTP 5XX).
    """

    def __init__(self, error_response: Dict):
        self.type = error_response.get('type', 'server_error')
        self.errors = error_response.get('errors', [])
        self.status_code = error_response.get('status_code', 500)

        message = f"Server error (HTTP {self.status_code}): {self.errors}"
        super().__init__(message)


class RateLimitError(CryptoHoodAPIError):
    """
    Raised when API rate limits are exceeded.
    """

    def __init__(self, reset_time: Optional[int] = None):
        self.reset_time = reset_time
        message = "Rate limit exceeded"
        if reset_time:
            message += f". Try again after {reset_time} seconds"
        super().__init__(message)


class OrderError(CryptoHoodAPIError):
    """
    Raised when there's an error related to order placement or manipulation.
    """

    def __init__(self, message: str, order_id: Optional[str] = None):
        self.order_id = order_id
        super().__init__(f"Order error: {message}")


class InsufficientFundsError(OrderError):
    """
    Raised when there are insufficient funds to place an order.
    """

    def __init__(self, required_amount: str, available_amount: str, currency: str):
        self.required_amount = required_amount
        self.available_amount = available_amount
        self.currency = currency
        message = (f"Insufficient funds: Required {required_amount} {currency}, "
                   f"but only {available_amount} {currency} available")
        super().__init__(message)


class InvalidSymbolError(ValidationError):
    """
    Raised when an invalid trading symbol is provided.
    """

    def __init__(self, symbol: str):
        message = f"Invalid trading symbol: {symbol}"
        super().__init__({'type': 'validation_error', 'errors': [{'attr': 'symbol', 'detail': message}]})


class WebSocketError(CryptoHoodAPIError):
    """
    Raised when there's an error with WebSocket connections.
    """

    def __init__(self, message: str, code: Optional[int] = None):
        self.code = code
        super().__init__(f"WebSocket error: {message}")


# Usage example:
"""
try:
    # Some API call
    response = client.place_order(...)
except ValidationError as e:
    print(f"Validation failed: {e}")
    field_errors = e.get_field_errors()
    for field, error in field_errors.items():
        print(f"{field}: {error}")
except InsufficientFundsError as e:
    print(f"Not enough funds: {e}")
    print(f"Required: {e.required_amount} {e.currency}")
    print(f"Available: {e.available_amount} {e.currency}")
except RateLimitError as e:
    print(f"Rate limit hit: {e}")
    if e.reset_time:
        print(f"Try again after {e.reset_time} seconds")
except ClientError as e:
    print(f"Client error: {e}")
    print(f"Status code: {e.status_code}")
except ServerError as e:
    print(f"Server error: {e}")
except CryptoHoodAPIError as e:
    print(f"General API error: {e}")
"""


class OrderError(CryptoHoodAPIError):
    """
    Raised when there's an error related to order placement or manipulation.
    """

    def __init__(self, message: str, order_id: Optional[str] = None):
        self.order_id = order_id
        super().__init__(f"Order error: {message}")
