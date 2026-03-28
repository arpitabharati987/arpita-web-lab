from sqlalchemy.orm import Session
from .. import models, schemas, auth
from app.models import User

def register_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        return None

    if not auth.verify_password(user.password, db_user.password):
        return None

    token = auth.create_access_token({"sub": db_user.username})

    return token



def get_all_users(db):
    return db.query(User).all()