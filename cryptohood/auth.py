import base64
import time
from typing import Dict
from nacl.signing import SigningKey, VerifyKey
from .exceptions import AuthenticationError


class CryptoHoodAuth:
    """
    Handles authentication for the Robinhood Crypto API.

    Attributes:
        api_key (str): The API key from Robinhood API Credentials Portal
        private_key (SigningKey): NaCl signing key generated from private key seed
        public_key (VerifyKey): NaCl verify key for signature verification
    """

    def __init__(self, api_key: str, private_key_base64: str, public_key_base64: str = None):
        """
        Initialize the authentication handler.

        Args:
            api_key (str): Your Robinhood API key
            private_key_base64 (str): Base64 encoded private key
            public_key_base64 (str): Optional base64 encoded public key for verification
        """
        self.api_key = api_key

        try:
            # Convert base64 private key to seed
            private_key_seed = base64.b64decode(private_key_base64)
            self.private_key = SigningKey(private_key_seed)

            # If public key is provided, set up verification
            if public_key_base64:
                public_key_bytes = base64.b64decode(public_key_base64)
                self.public_key = VerifyKey(public_key_bytes)
            else:
                self.public_key = self.private_key.verify_key

        except Exception as e:
            raise AuthenticationError(f"Failed to initialize authentication: {str(e)}")

    def _get_timestamp(self) -> int:
        """Get current UTC timestamp in seconds."""
        return int(time.time())

    def generate_headers(self, method: str, path: str, body: str = "") -> Dict[str, str]:
        """
        Generate authentication headers for API requests.

        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): API endpoint path
            body (str): Request body (if any)

        Returns:
            Dict[str, str]: Headers containing authentication information
        """
        timestamp = self._get_timestamp()

        try:
            # Create message to sign
            message = f"{self.api_key}{timestamp}{path}{method}{body}"

            # Sign the message
            signed = self.private_key.sign(message.encode("utf-8"))

            # Generate signature
            signature = base64.b64encode(signed.signature).decode("utf-8")

            # Verify signature if public key is available
            if self.public_key:
                self.public_key.verify(signed.message, signed.signature)

            # Return headers
            return {
                "x-api-key": self.api_key,
                "x-signature": signature,
                "x-timestamp": str(timestamp),
                "Content-Type": "application/json"
            }

        except Exception as e:
            raise AuthenticationError(f"Failed to generate authentication headers: {str(e)}")

    def verify_signature(self, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature using the public key.

        Args:
            message (bytes): The original message
            signature (bytes): The signature to verify

        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            self.public_key.verify(message, signature)
            return True
        except Exception:
            return False

    @staticmethod
    def is_timestamp_valid(timestamp: int, max_age: int = 30) -> bool:
        """
        Check if a timestamp is within the valid window (30 seconds by default).

        Args:
            timestamp (int): Timestamp to check
            max_age (int): Maximum age in seconds (default: 30)

        Returns:
            bool: True if timestamp is valid, False otherwise
        """
        current_time = int(time.time())
        return abs(current_time - timestamp) <= max_age
