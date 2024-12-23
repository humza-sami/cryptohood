# CryptoHood 

[![PyPI version](https://badge.fury.io/py/cryptohood.svg)](https://badge.fury.io/py/cryptohood)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A powerful and user-friendly Python wrapper for the Robinhood Crypto API. Trade cryptocurrencies programmatically with ease!

## 🚀 Quick Start

### Installation

```bash
pip install cryptohood
```

### Basic Usage

```python
from cryptohood import CryptoHood

# Initialize the client
client = CryptoHood(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Get crypto quotes
btc_quote = client.get_crypto_quotes("BTC")
print(f"Current BTC price: ${btc_quote['price']}")

# Place a buy order
order = client.place_order(
    symbol="BTC",
    quantity=0.1,
    side="buy"
)

# Check order status
status = client.get_order_status(order['id'])
print(f"Order status: {status}")
```

## 📚 Documentation

For detailed documentation, visit [Soon]

### Key Features Documentation

* Authentication
* Market Data
* Trading
* Account Management
* Error Handling

## 📝 Example Scripts

Check out the `examples` directory for more usage examples:
* Basic usage: `examples/basic_usage.py`
* Market data streaming: `examples/stream_data.py`
* Automated trading: `examples/auto_trader.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This package is unofficial and not affiliated with Robinhood. Use at your own risk. Always verify your trading logic and test thoroughly before using in production.

## 📞 Support

* Create an issue on GitHub
* Email: humzasami20@gmail.com



Made with ❤️ by Humza Sami
