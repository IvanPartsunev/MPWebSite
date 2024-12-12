import bcrypt
import datetime
import logging
import exceptions.users
import configuration
import db.connection
import db.models

from logging.handlers import RotatingFileHandler
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, Request
from sqlalchemy import delete, or_, update



def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def _check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(first_name: str, last_name: str, email: str, phone_number:int, password: str):
    with db.connection.get_session() as session:
        if get_user(email=email, phone_number=phone_number):
            raise exceptions.users.UserAlreadyExists()
        else:
            new_user = db.models.User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=_hash_password(password)
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user


def get_user(*, user_id: str = None, phone_number: int = None, email: str = None) -> db.models.User | None:
    with db.connection.get_session() as session:
        query = session.query(db.models.User)
        filters = []

        if user_id:
            filters.append(db.models.User.id == user_id)
        if phone_number:
            filters.append(db.models.User.phone_number == phone_number)
        if email:
            filters.append(db.models.User.email == email)

        if filters:
            query = query.filter(or_(*filters))

        user = query.first()

    return user


def sign_in(email: str, password: str | None = None):
    if user := get_user(email=email):
        if password and not _check_password(password, user.password):
            raise exceptions.users.WrongCredentialsException()
        access_payload = {"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60), "sub": str(user.id)}
        if user.role:
            access_payload["role"] = user.role.role.name
        jwt_config = configuration.JWT()
        access_token = jwt.encode(access_payload, key=jwt_config.key, algorithm=jwt_config.algorithm)

        refresh_payload = {
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7),  # 7 days
            "sub": str(user.id),
        }
        refresh_token = jwt.encode(refresh_payload, key=jwt_config.key, algorithm=jwt_config.algorithm)

        return access_token, refresh_token

    else:
        raise exceptions.users.UserDoesNotExistException()


def get_new_access_token(request: Request):
    jwt_config = configuration.JWT()
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, key=jwt_config.key, algorithms=[jwt_config.algorithm])

        access_payload = {
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),  # 1 hour
            "sub": payload["sub"],
        }
        access_token = jwt.encode(access_payload, key=jwt_config.key, algorithm=jwt_config.algorithm)

        return access_token

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

def get_users():
    with db.connection.get_session() as session:
        return session.query(db.models.User).all()


def add_user_to_role(user_id: str, role_id: str, added_by: str):
    with db.connection.get_session() as session:
        user_to_role = db.models.UserRole(user_id=user_id, role_id=role_id, added_by=added_by)
        session.add(user_to_role)
        session.commit()
        session.refresh(user_to_role)
        return user_to_role


def remove_user_from_role(user_id: str, role_id: str):
    with db.connection.get_session() as session:
        stmt = delete(db.models.UserRole).where(db.models.UserRole.role_id == role_id, db.models.UserRole.user_id == user_id)
        session.execute(stmt)
        session.commit()


def update_user(user_id: str, field: str, value: str):
    if field == 'password':
        value = _hash_password(password=value)

    with db.connection.get_session() as session:
        session.execute(update(db.models.User), [{"id": user_id, field: value}])
        session.commit()


logger = logging.getLogger("debug")
log_file = configuration.ROOT_PATH / 'logs' / "debug.log"
handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


