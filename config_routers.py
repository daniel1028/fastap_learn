from fastapi import APIRouter

from config.config import config

config_bp = APIRouter()


@config_bp.get("/config")
def get_config():
    return {
        "DEBUG": config.DEBUG,
        "SECRET_KEY": config.SECRET_KEY
    }
