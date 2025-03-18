# middleware.py
from fastapi import Request
from fastapi.responses import Response
from .context import tracking_id_var
import uuid

def init_middleware(app):
    @app.middleware("http")
    async def tracking_id_middleware(request: Request, call_next):
        # Extract tracking_id from headers or generate a new one
        tracking_id = request.headers.get("X-Tracking-ID", str(uuid.uuid4()))
        # Set the tracking_id in the context variable
        token = tracking_id_var.set(tracking_id)
        try:
            response = await call_next(request)
        finally:
            # Reset the context variable to its previous state
            tracking_id_var.reset(token)
        # Include the tracking_id in the response headers
        response.headers["X-Tracking-ID"] = tracking_id
        return response
