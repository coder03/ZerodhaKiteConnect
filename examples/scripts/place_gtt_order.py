import os
import json
import logging
from dotenv import load_dotenv
from kiteconnect import KiteConnect


class KiteTrader:
    """
    A wrapper class for KiteConnect to handle authentication and trading operations.
    """

    def __init__(self):
        """Initialize KiteConnect client with credentials from environment variables."""
        load_dotenv()

        self.api_key = os.getenv("KITE_API_KEY")
        self.access_token = os.getenv("KITE_ACCESS_TOKEN", "your_access_token_here")

        if not self.api_key:
            raise ValueError("KITE_API_KEY not found in environment variables")

        if not self.access_token or self.access_token == "your_access_token_here":
            raise ValueError("env KITE_ACCESS_TOKEN not found,\n"
                             "To get access token, you need to run flask_app.py and login to your account.\n"
                             "set using: export KITE_ACCESS_TOKEN=your_access_token_here.")

        try:
            self.kite = KiteConnect(api_key=self.api_key)
            self.kite.set_access_token(self.access_token)

            # Test connection
            profile = self.kite.profile()
            logging.info(f"Successfully connected to Kite for user: {profile['user_name']}")

        except Exception as e:
            logging.error(f"Failed to initialize Kite client: {e}")
            raise

    def place_gtt_order(self, tradingsymbol, exchange, quantity, price, last_price,
                       product="CNC", order_type="LIMIT"):
        """
        Place a single-leg GTT (Good Till Triggered) order.

        Args:
            tradingsymbol: Trading symbol (default: "SBIN")
            exchange: Exchange name (default: "NSE")
            quantity: Quantity to buy (default: 1)
            price: Trigger and order price (default: 470)
            last_price: Current market price (default: 473)
            product: Product type (default: "CNC")

        Returns:
            dict: GTT order response with trigger_id if successful, None if failed
        """
        try:
            order_single = [{
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "transaction_type": self.kite.TRANSACTION_TYPE_BUY,
                "quantity": quantity,
                "order_type": order_type,
                "product": product,
                "price": price,
            }]

            single_gtt = self.kite.place_gtt(
                trigger_type=self.kite.GTT_TYPE_SINGLE,
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                trigger_values=[price],
                last_price=last_price,
                orders=order_single
            )

            logging.info(f"GTT order placed with trigger_id: {single_gtt['trigger_id']}")
            # Pretty print order details
            print("\n" + "="*50)
            print("GTT ORDER DETAILS")
            print("="*50)
            print(f"Trading Symbol: {tradingsymbol}")
            print(f"Quantity      : {quantity}")
            print(f"Trigger Price : ₹{price}")
            print(f"Order Type    : {order_type}")
            print("="*50)
            return single_gtt

        except Exception as e:
            logging.error(f"Error placing GTT order: {e}")
            return None


# Usage example
if __name__ == "__main__":
    try:
        # Initialize trader once
        trader = KiteTrader()

        # Place GTT order
        result = trader.place_gtt_order(
            tradingsymbol="SBIN",
            exchange="NSE",
            quantity=1,
            price=471,
            last_price=500,
            product="CNC",
            order_type="LIMIT"
        )
        if result:
            print(f"GTT order placed successfully placed with trigger_id: {result['trigger_id']}")


    except Exception as e:
        print(f"Application error: {e}")