#!/usr/bin/env python3
''' authentication '''
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' register new if not exists '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed)
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        ''' validate password  '''
        try:
            usr = self._db.find_user_by(email=email)
        except Exception:
            return False
        if bcrypt.checkpw(password.encode("utf-8"), usr.hashed_password):
            return True
        return False


def _hash_password(password: str) -> bytes:
    ''' hash password by bcrypt '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid():
    ''' generate uuid '''
    return str(uuid.uuid4())
