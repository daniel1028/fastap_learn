import logging
import os
from pydantic_settings import BaseSettings
from utils.exceptions import CustomException
import requests
# Load environment variables
ENV_FILE = os.getenv("ENV_FILE", ".env")
CONFIG_SERVER_HOST = os.getenv("CONFIG_SERVER_HOST", "http://localhost:8001")

logger = logging.getLogger("config_app")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Config(BaseSettings):
    DEBUG: bool = False

    class Config:
        env_file = ENV_FILE
        extra = "allow"


class BaseConfig(Config):
    CONFIG_URL: str = f"{CONFIG_SERVER_HOST}/config-management/config"
    _cached_config = None

    def get_config(self, force_refresh=False):
        """ Fetches config from cache or loads it once from the server. """
        if self._cached_config is None or force_refresh:
            self.refresh_config()
        return self._cached_config

    def refresh_config(self):
        """ Refreshes the cached config from the config server. """
        try:
            logger.info(f"Fetching config from: {self.CONFIG_URL}")
            response = requests.get(self.CONFIG_URL)
            response.raise_for_status()
            self._cached_config = response.json()
        except requests.RequestException as e:
            raise CustomException(f"Unable to read config server: {e}")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


# Determine environment and load appropriate config
env = os.getenv("ENV", "development")

if env == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

# Fetch config once on startup
config.refresh_config()

logger.info(f"Loaded config from: {ENV_FILE}")
logger.info(f"DEBUG: {config.DEBUG}")
