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

    def create_session(self, email: str) -> str:
        ''' create a session id for the email provided '''
        try:
            usr = self._db.find_user_by(email=email)
        except Exception:
            return None
        session = _generate_uuid()
        self._db.update_user(usr.id, session_id=session)
        return usr.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        ''' return user by session id '''
        try:
            usr = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return usr

    def destroy_session(self, user_id: int) -> None:
        ''' destroy sesion id by user id '''
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        ''' reset token '''
        try:
            usr = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(usr.id, reset_token=reset_token)
        return usr.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        ''' update password '''
        usr = self._db.find_user_by(reset_token=reset_token)
        if not usr:
            raise ValueError()
        hashed_password = _hash_password(password)
        self._db.update_user(usr.id, hashed_password=hashed_password)
        self._db.update_user(usr.id, reset_token=None)
        return None


def _hash_password(password: str) -> bytes:
    ''' hash password by bcrypt '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    ''' generate uuid '''
    return str(uuid.uuid4())
