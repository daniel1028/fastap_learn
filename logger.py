import logging
from logging.handlers import RotatingFileHandler

from config.config import config
from config.context import tracking_id_var


class ContextFilter(logging.Filter):
    def filter(self, record):
        # Retrieve the tracking_id from the context variable
        record.tracking_id = tracking_id_var.get()
        return True

print("sdkjhsdf;khsdfglkjfhd")
# Configure logging
logger = logging.getLogger("user_management_app")
logger.setLevel(logging.DEBUG)

# Create a formatter that includes the tracking_id
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(tracking_id)s - %(message)s")

# File handler with rotation
file_handler = RotatingFileHandler(f"{config.get_config()["LOG_PATH"]}/user_management_app.log",
                                   maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(formatter)
file_handler.addFilter(ContextFilter())
logger.addHandler(file_handler)

# Stream handler (logs to console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.addFilter(ContextFilter())
logger.addHandler(console_handler)
