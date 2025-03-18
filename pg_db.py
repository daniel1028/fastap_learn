import logging

import asyncpg

from config.config import config


class PGDatabase:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            try:
                logging.info("Creating a new database connection pool...")
                cls._instance = await asyncpg.create_pool(config.get_config()['DB_URL'])
            except Exception as e:
                logging.error(f"Database connection error: {e}")
                raise
        return cls._instance

    @classmethod
    async def close(cls):
        if cls._instance:
            logging.info("Closing database connection pool...")
            await cls._instance.close()
            cls._instance = None
