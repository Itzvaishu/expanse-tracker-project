import sys
import os

# add the project root directory to the sys.path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal, engine
from app.db.base import Base 
from app.models import Role, Permission, User, Category 

print("🚀 Script Started...")

def init_db():
    # 1. Create Tablescls
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 2. Create Permissions
        permissions = ["category:delete", "settings:view"]
        for slug in permissions:
            if not db.query(Permission).filter_by(slug=slug).first():
                new_perm = Permission(name=slug.replace(":", " ").title(), slug=slug)
                db.add(new_perm)
                print(f"➕ Permission Added: {slug}")
        db.commit()

        # 3. Create Roles
        # Permissions fetch for role assignment
        perm_delete = db.query(Permission).filter_by(slug="category:delete").first()
        
        # Admin Role
        if not db.query(Role).filter_by(name="admin").first():
            admin = Role(name="admin")
            if perm_delete: admin.permissions.append(perm_delete)
            db.add(admin)
            print("➕ Role Added: admin")

        # User Role
        if not db.query(Role).filter_by(name="user").first():
            user = Role(name="user")
            db.add(user)
            print("➕ Role Added: user")
        
        db.commit()

        # 4. Global Categories
        default_cats = ["Food", "Transport", "Utilities", "Entertainment", "Salary", "Health"]
        for cat_name in default_cats:
            exists = db.query(Category).filter(Category.name == cat_name, Category.user_id == None).first()
            if not exists:
                new_cat = Category(name=cat_name, user_id=None)
                db.add(new_cat)
                print(f"➕ Global Category: {cat_name}")

        db.commit()
        print("\n🎉 SUCCESS! Database Setup Complete.")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()