import uuid
from fastapi import APIRouter, status, Request

from config.config import config
from database.pg_db import PGDatabase
from utils.logger import logger
from utils.response_handler import success_response, error_response

user_mgmt_bp = APIRouter()


@user_mgmt_bp.get("/test", status_code=status.HTTP_200_OK)
async def test(request: Request):
    tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
    logger.info(f"[{tracking_id}] Received user management request for test")
    return {"message": "User Management service is working"}


@user_mgmt_bp.get("/test_db", status_code=status.HTTP_200_OK)
async def test_db(request: Request):
    tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
    logger.info(f"[{tracking_id}] Received user management request for test_db")
    pool = await PGDatabase.get_instance()
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'FINTECH'")
        return {"message": "User Management service is working", "result": [r['table_name'] for r in result]}


@user_mgmt_bp.get("/refresh-config", status_code=status.HTTP_200_OK)
async def refresh_config(request: Request):
    tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
    logger.info(f"[{tracking_id}] Received user management request for test_db")
    try:
        config_json = config.get_config(force_refresh=True)
        return success_response(config_json, status.HTTP_200_OK)
    except Exception as e:
        return error_response(f"Unable to refresh the config : {e}", 500)


@user_mgmt_bp.get("/users", status_code=status.HTTP_200_OK)
async def get_users(request: Request, ):
    tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
    logger.info(f"[{tracking_id}] Received user management request for get_users")
    users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]
    return success_response(users, status.HTTP_200_OK)


@user_mgmt_bp.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, data: dict):
    tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
    logger.info(f"[{tracking_id}] Received user management request for create_user")
    return success_response(data, status.HTTP_201_CREATED)
