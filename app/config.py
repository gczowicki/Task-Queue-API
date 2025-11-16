import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskqueue:taskqueue123@localhost:5432/taskqueue_db"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

print(f"DATABASE_URL loaded: {DATABASE_URL}")
print(f"REDIS_URL loaded: {REDIS_URL}")