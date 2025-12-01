from app.db.session import SessionLocal
from app.services.auth_service import create_user
from app.schemas.user_schema import UserCreate

def add_docs_user():
    db = SessionLocal()
    try:
        user_data = UserCreate(
            username="docs",
            email="docs@example.com",
            password="docs123",
            full_name="Docs User"
        )
        user = create_user(db=db, user=user_data)
        print(f"User 'docs' created with ID: {user.id}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_docs_user()
