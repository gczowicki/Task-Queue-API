from venv import logger
from app.database import create_tables
from app import models # noqa - import needed for SQLAlchemy to register models

if __name__ == "__main__":
    logger.info("Creating database tables...")
    create_tables()
    logger.info("Tables created successfully!")