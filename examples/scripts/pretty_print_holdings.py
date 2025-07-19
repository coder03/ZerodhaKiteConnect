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

    def get_holdings(self):
        """Fetch and return holdings data."""
        try:
            holdings = self.kite.holdings()
            return holdings
        except Exception as e:
            logging.error(f"Error fetching holdings: {e}")
            return None

    def get_holdings_and_pretty_print(self):
        """Fetch and return holdings data in a formatted table."""
        try:
            holdings = self.kite.holdings()

            if not holdings:
                print("No holdings found.")
                return holdings

            # Print table header
            print("\n" + "="*90)
            print("HOLDINGS SUMMARY")
            print("="*90)
            print(f"{'Symbol':<15} {'Avg Price':<12} {'Quantity':<10} {'Last Price':<12} {'P&L':<12} {'Day Change %':<12}")
            print("-"*90)

            total_pnl = 0

            for holding in holdings:
                symbol = holding['tradingsymbol']
                avg_price = holding['average_price']
                quantity = holding['realised_quantity']
                last_price = holding['last_price']
                pnl = holding['pnl']
                day_change_pct = holding['day_change_percentage']

                total_pnl += pnl

                # Format values for better display with right-aligned prices for decimal alignment
                avg_price_str = f"₹{avg_price:>8.2f}"
                last_price_str = f"₹{last_price:>8.2f}"
                pnl_str = f"₹{pnl:>8.2f}"
                day_change_str = f"{day_change_pct:>6.2f}%"

                # Color coding for P&L (optional - works in terminal)
                if pnl >= 0:
                    pnl_display = f"\033[92m{pnl_str}\033[0m"  # Green for profit
                else:
                    pnl_display = f"\033[91m{pnl_str}\033[0m"  # Red for loss

                print(f"{symbol:<15} {avg_price_str:<12} {quantity:<10} {last_price_str:<12} {pnl_display:<20} {day_change_str:<12}")

            print("-"*90)
            total_pnl_str = f"₹{total_pnl:.2f}"
            if total_pnl >= 0:
                total_display = f"\033[92m{total_pnl_str}\033[0m"
            else:
                total_display = f"\033[91m{total_pnl_str}\033[0m"

            print(f"{'TOTAL P&L:':<52} {total_display}")
            print("="*90)

            return holdings

        except Exception as e:
            logging.error(f"Error fetching holdings: {e}")
            return None

    def get_orders(self):
        """Fetch and return orders data."""
        try:
            orders = self.kite.orders()
            return orders
        except Exception as e:
            logging.error(f"Error fetching orders: {e}")
            return None

    def display_holdings_and_orders(self):
        """Display holdings and orders in formatted JSON."""
        holdings = self.get_holdings()
        orders = self.get_orders()

        if holdings is not None:
            print("Holdings:")
            print(json.dumps(holdings, indent=4))

        if orders is not None:
            print("\nOrders:")
            print(json.dumps(orders, indent=4))

        return {"holdings": holdings, "orders": orders}

# Usage example
if __name__ == "__main__":
    try:
        # Initialize trader once
        trader = KiteTrader()

        # Get and display holdings/orders
        #trader.display_holdings_and_orders()

        # Get and display holdings in a pretty format
        trader.get_holdings_and_pretty_print()

    except Exception as e:
        print(f"Application error: {e}")