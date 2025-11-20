import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskqueue:taskqueue123@localhost:5432/taskqueue_db"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)