import datetime
import logging
from logging.handlers import RotatingFileHandler

import bcrypt

import configuration
import db.connection
import db.models
from sqlalchemy import delete, or_, update
import exceptions.users
from jose import jwt


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def _check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(first_name: str, last_name: str, email: str, phone_number:int, password: str):
    with db.connection.get_session() as session:
        if get_user(username=username, email=email):
            raise exceptions.users.UserAlreadyExists()
        else:
            new_user = db.models.User(
                first_name=first_name,
                last_name=last_name,
                email=email, phone_number=phone_number,
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


def sign_in(username: str, password: str | None = None) -> str:
    if user := get_user(username=username):
        if password and not _check_password(password, user.password):
            raise exceptions.users.WrongCredentialsException()
        payload = {"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60), "sub": str(user.id)}
        if user.roles:
            payload["roles"] = user.roles
        jwt_config = configuration.JWT()
        return jwt.encode(payload, key=jwt_config.key, algorithm=jwt_config.algorithm)
    else:
        raise exceptions.users.UserDoesNotExistException()


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


def update_user_tokens(user_id, tokens):
    with db.connection.get_session() as session:
        user = session.query(db.models.User).where(db.models.User.id == user_id).first()
        user.tokens = tokens
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


