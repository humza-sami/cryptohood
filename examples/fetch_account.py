from cryptohood import CryptoHood

# Your API credentials
API_KEY = "your-api-key"
PRIVATE_KEY = "your-private-key-base64"

# Initialize the client
client = CryptoHood(api_key=API_KEY, private_key=PRIVATE_KEY)

# Get account information
account = client.get_account()
