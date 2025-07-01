from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import UserCreate, UserUpdate, UserPatch
from typing import List, Optional
from auth import get_password_hash

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        nickname=user.nickname,
        password=hashed_password,
        about_me=user.about_me,
        gender=user.gender,
        birthdate=user.birthdate,
        favorites=user.favorites
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists")

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """Update user with PUT method (full update)"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    
    # Check for unique constraints
    if 'username' in update_data:
        existing_user = get_user_by_username(db, update_data['username'])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Username already exists")
    
    if 'email' in update_data:
        existing_user = get_user_by_email(db, update_data['email'])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already exists")
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Update failed due to constraint violation")

def patch_user(db: Session, user_id: int, user: UserPatch) -> Optional[User]:
    """Update user with PATCH method (partial update)"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    
    # Check for unique constraints
    if 'username' in update_data:
        existing_user = get_user_by_username(db, update_data['username'])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Username already exists")
    
    if 'email' in update_data:
        existing_user = get_user_by_email(db, update_data['email'])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already exists")
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Update failed due to constraint violation")

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user by ID"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True 