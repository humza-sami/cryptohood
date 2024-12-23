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
