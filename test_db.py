from app.db.session import SessionLocal

def test_db_connection():
    try:
        db = SessionLocal()
        result = db.execute("SELECT 1").fetchone()
        print("Database connection successful! Result:", result)
        db.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_db_connection()
