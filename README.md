# CryptoHood

[![PyPI version](https://badge.fury.io/py/cryptohood.svg)](https://badge.fury.io/py/cryptohood)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A powerful and user-friendly Python wrapper for the Robinhood Crypto API. Trade cryptocurrencies programmatically with ease!

##  Quick Start

### Installation

```bash
pip install cryptohood
```

### Basic Usage

```python
from cryptohood import CryptoHood
from datetime import datetime, timedelta

# Your API credentials
API_KEY = "your-api-key"
PRIVATE_KEY = "your-private-key-base64"

client = CryptoHood(api_key=API_KEY, private_key=PRIVATE_KEY)

# Get orders from last 24 hours
start_time = datetime.utcnow() - timedelta(days=1)

orders = client.get_orders(created_at_start=start_time)

print(orders)

```

## Documentation

For detailed documentation, visit [Soon]

### Key Features Documentation

- Authentication
- Market Data
- Trading
- Account Management
- Error Handling

## Example Scripts

Check out the `examples` directory for more usage examples:

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This package is unofficial and not affiliated with Robinhood. Use at your own risk. Always verify your trading logic and test thoroughly before using in production.

## 📞 Support

- Create an issue on GitHub
- Email: humzasami20@gmail.com

Made with ❤️ by Humza Sami
