from contextvars import ContextVar

# Create a ContextVar for tracking_id
tracking_id_var = ContextVar('tracking_id', default='N/A')