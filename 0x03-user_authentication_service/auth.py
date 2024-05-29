#!/usr/bin/env python3
''' authentication '''
import bcrypt
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


def _hash_password(password: str) -> bytes:
    ''' hash password by bcrypt '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
