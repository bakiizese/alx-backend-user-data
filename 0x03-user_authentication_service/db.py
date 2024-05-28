"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, List
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        try:
            u1 = User(email=email, hashed_password=hashed_password)
            self._session.add(u1)
            self._session.commit()
        except Exception:
            self._session.rollback()
            u1 = None
        return u1

    def find_user_by(self, **kwargs) -> User:
        """ return whats found """
        if not kwargs:
            raise InvalidRequestError
        col = User.__table__.columns.keys()
        for k in kwargs.keys():
            if k not in col:
                raise InvalidRequestError
        qr = self._session.query(User).filter_by(**kwargs).first()
        if qr is None:
            raise NoResultFound
        return qr

    def update_user(self, ids: int, **kwargs) -> None:
        ''' update a value '''
        u1 = self.find_user_by(id=ids)
        if u1 is None:
            return
        cols = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                cols[getattr(User, k)] = v
            else:
                raise ValueError()
        
        self._session.query(User).filter(User.id == ids).update(
            cols,
            synchronize_session=False,
        )
        self._session.commit()