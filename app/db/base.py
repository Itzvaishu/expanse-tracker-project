from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # <-- THIS LINE CHANGED
from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()




password = "Qsefthuko321!@#"
encoded_password = quote(password)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@127.0.0.1/vaishudb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Now this function is imported from new location
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

