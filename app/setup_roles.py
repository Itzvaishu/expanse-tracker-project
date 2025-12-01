
import sys
import os

# Path setup
sys.path.append(os.getcwd())

print("hello world")
print("🚀 Script Started...")

try:
    from app.db.session import SessionLocal, engine
    
  
    from app.db.base import Base  # Base yahan se aayega
    from app.models import Role, Permission, Category # Models yahan se aayenge
    
    
    print("✅ Imports Successful")
except Exception as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def init_db():
    print("🔄 Connecting to Database...")
    
    try:
        # Create Tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables Verified/Created")
    except Exception as e:
        print(f"❌ Table Creation Failed: {e}")
        return

    db = SessionLocal()

    try:
        # 1. Permissions
        permissions = ["category:delete", "settings:view"]
        
        for slug in permissions:
            if not db.query(Permission).filter_by(slug=slug).first():
                new_perm = Permission(name=slug.replace(":", " ").title(), slug=slug)
                db.add(new_perm)
                print(f"➕ Permission Added: {slug}")
        
        db.commit()

        # 2. Roles
        # Fetch Permission
        delete_perm = db.query(Permission).filter_by(slug="category:delete").first()
        
        # Admin Role
        if not db.query(Role).filter_by(name="admin").first():
            admin = Role(name="admin")
            if delete_perm: admin.permissions.append(delete_perm)
            db.add(admin)
            print("➕ Role Added: admin")

        # User Role
        if not db.query(Role).filter_by(name="user").first():
            user = Role(name="user")
            db.add(user)
            print("➕ Role Added: user")

        db.commit()
        print("\n🎉 SUCCESS! Roles & Permissions Setup Complete.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()



        
        # --- 4. GLOBAL CATEGORIES ADD KARNA ---
        from app.models import Category # Ensure karein yeh upar import ho
        
        default_cats = ["Food", "Transport", "Utilities", "Entertainment", "Salary", "Health"]
        
        print("🔄 Checking Global Categories...")
        for cat_name in default_cats:
            # Check agar yeh Global category pehle se hai
            exists = db.query(Category).filter(Category.name == cat_name, Category.user_id == None).first()
            
            if not exists:
                # User ID = None ka matlab yeh Sabke liye hai
                new_cat = Category(name=cat_name, user_id=None) 
                db.add(new_cat)
                print(f"➕ Global Category Created: {cat_name}")
        
        db.commit()
        print("\n🎉 SUCCESS! Roles, Permissions & Categories Setup Complete.")        

if __name__ == "__main__":
    init_db()