# Quick usage with existing token
from kiteconnect import KiteConnect
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
# This access token is generated from the login flow, run
# `python examples/flask_app.py` and then click the link to generate access_token.
KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN", "your_access_token_here")
kite.set_access_token(KITE_ACCESS_TOKEN)
holdings = kite.holdings()
orders = kite.orders()
print(json.dumps(holdings, indent=4))