import json
from typing import List, Dict, Optional, Union, Any
import uuid
import requests
from datetime import datetime
from urllib.parse import urlencode
from .auth import CryptoHoodAuth
from .exceptions import (CryptoHoodAPIError, ValidationError, ClientError, ServerError, OrderError)


class CryptoHood:
    """
    Main client for interacting with Robinhood Crypto API.
    """

    def __init__(self, api_key: str, private_key: str, public_key: str = None):
        """
        Initialize the CryptoHood client.

        Args:
            api_key (str): Your Robinhood API key
            private_key (str): Base64 encoded private key
            public_key (str): Optional base64 encoded public key
        """
        self.base_url = "https://trading.robinhood.com"
        self.auth = CryptoHoodAuth(api_key, private_key, public_key)

    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Any:
        """
        Make an authenticated request to the Robinhood API.

        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            params (Dict): Query parameters
            data (Dict): Request body data

        Returns:
            Any: Response data
        """
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(data) if data else ""

        headers = self.auth.generate_headers(method, endpoint, body)

        try:
            response = requests.request(method=method, url=url, headers=headers, params=params, json=data)

            # Handle different status codes
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                error_type = error_data.get('type')

                if error_type == 'validation_error':
                    raise ValidationError(error_data)
                elif error_type == 'client_error':
                    raise ClientError(error_data)
                elif error_type == 'server_error':
                    raise ServerError(error_data)
                else:
                    raise CryptoHoodAPIError(f"Unknown error: {error_data}")

        except requests.exceptions.RequestException as e:
            raise CryptoHoodAPIError(f"Request failed: {str(e)}")

    def get_account(self) -> Dict:
        """
        Get Robinhood Crypto account details.

        Returns:
            Dict: Account information including:
                - account_number (str)
                - status (str): 'active', 'deactivated', or 'sell_only'
                - buying_power (str)
                - buying_power_currency (str)
        """
        endpoint = "/api/v1/crypto/trading/accounts/"
        return self._make_request("GET", endpoint)

    def get_best_bid_ask(self, symbols: Union[str, List[str]] = None) -> Dict:
        """
        Get best bid and ask prices for specified symbols.

        Args:
            symbols (Union[str, List[str]]): Single symbol or list of symbols (e.g., "BTC-USD")

        Returns:
            Dict: Best bid and ask prices for requested symbols
        """
        endpoint = "/api/v1/crypto/marketdata/best_bid_ask/"

        params = {}
        if symbols:
            if isinstance(symbols, str):
                symbols = [symbols]
            params = {"symbol": symbols}

        return self._make_request("GET", endpoint, params=params)

    def get_estimated_price(self, symbol: str, side: str, quantities: Union[str, List[str]]) -> Dict:
        """
        Get estimated price for specific symbol and quantities.

        Args:
            symbol (str): Trading pair symbol (e.g., "BTC-USD")
            side (str): Order side ("bid", "ask", or "both")
            quantities (Union[str, List[str]]): Quantities to estimate

        Returns:
            Dict: Estimated prices for requested quantities
        """
        endpoint = "/api/v1/crypto/marketdata/estimated_price/"

        if isinstance(quantities, list):
            quantities = ",".join(quantities)

        params = {"symbol": symbol, "side": side, "quantity": quantities}

        return self._make_request("GET", endpoint, params=params)

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str = None) -> Dict:
        """
        Place a crypto order.

        Args:
            symbol (str): Trading pair symbol (e.g., "BTC-USD")
            side (str): Order side ("buy" or "sell")
            order_type (str): Order type ("market" or "limit")
            quantity (str): Order quantity
            price (str, optional): Limit price (required for limit orders)

        Returns:
            Dict: Order details
        """
        endpoint = "/api/v1/crypto/trading/orders/"

        order_config = {"asset_quantity": quantity}
        if price and order_type == "limit":
            order_config["price"] = price

        data = {
            "client_order_id": str(uuid.uuid4()),
            "side": side,
            "type": order_type,
            "symbol": symbol,
            f"{order_type}_order_config": order_config
        }

        return self._make_request("POST", endpoint, data=data)

    def get_trading_pairs(self,
                          symbols: Optional[Union[str, List[str]]] = None,
                          limit: Optional[int] = None,
                          cursor: Optional[str] = None) -> Dict:
        """
        Get list of trading pairs.

        Args:
            symbols (Optional[Union[str, List[str]]]): Single symbol or list of symbols
            limit (Optional[int]): Number of results per page
            cursor (Optional[str]): Pagination cursor

        Returns:
            Dict: Trading pairs information with pagination
        """
        endpoint = "/api/v1/crypto/trading/trading_pairs/"
        params = {}

        if symbols:
            if isinstance(symbols, str):
                symbols = [symbols]
            params['symbol'] = symbols

        if limit:
            params['limit'] = limit

        if cursor:
            params['cursor'] = cursor

        return self._make_request("GET", endpoint, params=params)

    def get_holdings(self,
                     asset_codes: Optional[Union[str, List[str]]] = None,
                     limit: Optional[int] = None,
                     cursor: Optional[str] = None) -> Dict:
        """
        Get cryptocurrency holdings for current user.

        Args:
            asset_codes (Optional[Union[str, List[str]]]): Single asset code or list of codes
            limit (Optional[int]): Number of results per page
            cursor (Optional[str]): Pagination cursor

        Returns:
            Dict: Holdings information with pagination
        """
        endpoint = "/api/v1/crypto/trading/holdings/"
        params = {}

        if asset_codes:
            if isinstance(asset_codes, str):
                asset_codes = [asset_codes]
            params['asset_code'] = asset_codes

        if limit:
            params['limit'] = limit

        if cursor:
            params['cursor'] = cursor

        return self._make_request("GET", endpoint, params=params)

    def get_orders(self,
                   created_at_start: Optional[Union[str, datetime]] = None,
                   created_at_end: Optional[Union[str, datetime]] = None,
                   updated_at_start: Optional[Union[str, datetime]] = None,
                   updated_at_end: Optional[Union[str, datetime]] = None,
                   symbol: Optional[str] = None,
                   order_id: Optional[str] = None,
                   side: Optional[str] = None,
                   state: Optional[str] = None,
                   order_type: Optional[str] = None,
                   limit: Optional[int] = None,
                   cursor: Optional[str] = None) -> Dict:
        """
        Get list of orders for current user.

        Args:
            created_at_start (Optional[Union[str, datetime]]): Filter by creation start time
            created_at_end (Optional[Union[str, datetime]]): Filter by creation end time
            updated_at_start (Optional[Union[str, datetime]]): Filter by update start time
            updated_at_end (Optional[Union[str, datetime]]): Filter by update end time
            symbol (Optional[str]): Trading pair symbol (e.g., "BTC-USD")
            order_id (Optional[str]): Specific order ID
            side (Optional[str]): "buy" or "sell"
            state (Optional[str]): Order state ("open", "canceled", "partially_filled", "filled", "failed")
            order_type (Optional[str]): Order type ("limit", "market", "stop_limit", "stop_loss")
            limit (Optional[int]): Number of results per page
            cursor (Optional[str]): Pagination cursor

        Returns:
            Dict: Orders information with pagination
        """
        endpoint = "/api/v1/crypto/trading/orders/"
        params = {}

        # Helper function to format datetime objects
        def format_datetime(dt):
            if isinstance(dt, datetime):
                return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            return dt

        # Add parameters if they are provided
        if created_at_start:
            params['created_at_start'] = format_datetime(created_at_start)
        if created_at_end:
            params['created_at_end'] = format_datetime(created_at_end)
        if updated_at_start:
            params['updated_at_start'] = format_datetime(updated_at_start)
        if updated_at_end:
            params['updated_at_end'] = format_datetime(updated_at_end)
        if symbol:
            params['symbol'] = symbol.upper()
        if order_id:
            params['id'] = order_id
        if side:
            if side not in ['buy', 'sell']:
                raise ValidationError({'errors': [{'attr': 'side', 'detail': 'Must be either "buy" or "sell"'}]})
            params['side'] = side
        if state:
            valid_states = ['open', 'canceled', 'partially_filled', 'filled', 'failed']
            if state not in valid_states:
                raise ValidationError({'errors': [{'attr': 'state', 'detail': f'Must be one of: {", ".join(valid_states)}'}]})
            params['state'] = state
        if order_type:
            valid_types = ['limit', 'market', 'stop_limit', 'stop_loss']
            if order_type not in valid_types:
                raise ValidationError({'errors': [{'attr': 'type', 'detail': f'Must be one of: {", ".join(valid_types)}'}]})
            params['type'] = order_type
        if limit:
            params['limit'] = limit
        if cursor:
            params['cursor'] = cursor

            return self._make_request("GET", endpoint, params=params)

        def get_paginated_results(self, initial_response: Dict) -> List:
            """
            Helper method to get all paginated results.

            Args:
                initial_response (Dict): Initial API response with pagination

            Returns:
                List: All combined results
            """
            all_results = initial_response.get('results', [])
            next_url = initial_response.get('next')

            while next_url:
                # Extract endpoint and params from next_url
                path = next_url.split(self.base_url)[-1]
                response = self._make_request("GET", path)
                all_results.extend(response.get('results', []))
                next_url = response.get('next')

            return all_results

        def get_all_holdings(self, asset_codes: Optional[Union[str, List[str]]] = None) -> List:
            """
            Get all holdings without pagination.

            Args:
                asset_codes (Optional[Union[str, List[str]]]): Single asset code or list of codes

            Returns:
                List: All holdings
            """
            initial_response = self.get_holdings(asset_codes=asset_codes)
            return self.get_paginated_results(initial_response)

        def get_all_orders(self, **kwargs) -> List:
            """
            Get all orders without pagination.

            Args:
                **kwargs: Same parameters as get_orders()

            Returns:
                List: All orders
            """
            initial_response = self.get_orders(**kwargs)
            return self.get_paginated_results(initial_response)

    def cancel_order(self, order_id: str) -> str:
        """
        Cancel an open crypto trading order.

        Args:
            order_id (str): UUID of the order to cancel

        Returns:
            str: Success message with order ID

        Raises:
            ValidationError: If the order ID is invalid
            ClientError: If the order cannot be cancelled
            ServerError: If there's a server-side error
            OrderError: If the order is already cancelled or completed
        """
        endpoint = f"/api/v1/crypto/trading/orders/{order_id}/cancel/"

        try:
            response = self._make_request("POST", endpoint)

            # Handle text/plain response
            if isinstance(response, str):
                return response
            return f"Cancel request was submitted for order {order_id}"

        except ClientError as e:
            if e.status_code == 404:
                raise OrderError(f"Order {order_id} not found")
            elif "already cancelled" in str(e).lower():
                raise OrderError(f"Order {order_id} is already cancelled")
            elif "already completed" in str(e).lower():
                raise OrderError(f"Order {order_id} is already completed")
            raise
