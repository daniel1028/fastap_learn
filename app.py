from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import config
from config.middleware import init_middleware
from database.pg_db import PGDatabase
from routes.user_router import user_mgmt_bp
from utils.logger import logger


async def lifespan(app: FastAPI):
    logger.info(config.get_config())
    logger.info("Starting the application...")
    await PGDatabase.get_instance()
    yield
    await PGDatabase.close()

app = FastAPI(lifespan=lifespan)

init_middleware(app)

# Add CORS middleware correctly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_mgmt_bp, prefix="/user-management")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="debug" if config.get_config()['DEBUG'] else "info")
