"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ return user obj """
        u1 = User(email=email, hashed_password=hashed_password)
        self._session.add(u1)
        self._session.commit()

        return u1

    def find_user_by(self, **kwargs) -> User:
        """ return whats found """
        email = kwargs.get('email', None)
        if not email:
            raise InvalidRequestError
        qr = self._session.query(User).filter_by(email=email).first()
        if qr is None:
            raise NoResultFound
        return qr
