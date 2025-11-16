from app.database import create_tables
from app import models # noqa - import needed for SQLAlchemy to register models

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Tables created successfully!")