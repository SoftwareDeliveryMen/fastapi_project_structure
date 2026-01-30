"""Create a superuser from command line"""
import sys
from pathlib import Path
from getpass import getpass

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_superuser():
    """Interactive superuser creation"""
    print("Create Superuser")
    print("-" * 40)
    
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return
    
    db: Session = SessionLocal()
    
    try:
        # Check if user exists
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            print("❌ User with this username or email already exists!")
            return
        
        # Create superuser
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        
        print(f"✅ Superuser '{username}' created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()