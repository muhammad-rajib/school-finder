from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    *,
    name: str,
    email: str,
    password_hash: str,
    role: str,
    school_id: UUID | None,
) -> User:
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role,
        school_id=school_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_active_status(db: Session, user_id: UUID, is_active: bool) -> User | None:
    user = get_user_by_id(db, user_id)
    if user is None:
        return None

    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user
