from sqlalchemy import create_engine, inspect
from app.core.config import settings
from app.db.base import Base

# Import models so they're registered on Base.metadata
import app.models  # noqa: F401


def main():
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables present in database:", tables)


if __name__ == "__main__":
    main()
