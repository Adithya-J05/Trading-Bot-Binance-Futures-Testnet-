import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from .logging_config import logger

load_dotenv()

class BinanceTestnetClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            logger.error("API Credentials missing in environment variables.")
            raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment.")
        
        # Initialize python-binance client targeted at the Testnet
        self.client = Client(self.api_key, self.api_secret, testnet=True)
        logger.info("Binance Futures Testnet Client initialized successfully.")

    def place_futures_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """Dispatches orders safely to the Binance Futures Testnet."""
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }
        
        if order_type.upper() == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC" # Good 'Til Cancelled (Required for standard LIMIT orders)

        try:
            logger.info(f"Sending Request: {params}")
            # Use futures_create_order for USDT-M Futures execution
            response = self.client.futures_create_order(**params)
            logger.info(f"Received Response Success: {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: Status Code {e.status_code}, Message: {e.message}")
            raise e
        except Exception as e:
            logger.error(f"Network or unexpected error occurred: {str(e)}")
            raise e