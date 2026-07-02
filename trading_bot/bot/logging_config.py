import logging
import os

def setup_logging():
    """Sets up standard file logging for API requests, responses, and errors."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "bot.log")),
            logging.StreamHandler() # Also print to console via standard logging if needed
        ]
    )
    
    # Silence third-party verbose logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger("trading_bot")