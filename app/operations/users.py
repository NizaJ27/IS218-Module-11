from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        # Raise a ValueError so tests/handlers can convert to HTTP 400
        raise ValueError("username or email already exists") from e
    return user
