from .client import BinanceTestnetClient
from .validators import validate_inputs
from .logging_config import logger

class OrderManager:
    def __init__(self):
        self.client = BinanceTestnetClient()

    def execute(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """Validates inputs and coordinates order routing through the client wrapper."""
        # Step 1: Pre-execution validation
        validate_inputs(symbol, side, order_type, quantity, price)
        
        # Step 2: Order execution via client
        return self.client.place_futures_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )