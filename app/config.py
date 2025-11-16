import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskqueue:taskqueue123@localhost:5432/taskqueue_db"
)

print(f"DATABASE_URL loaded: {DATABASE_URL}") 