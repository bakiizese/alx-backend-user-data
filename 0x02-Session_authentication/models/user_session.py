#!/usr/bin/env python3
''' save sessions '''
from models.base import Base


class UserSession(Base):
    ''' users sessions '''
    def __init__(self, *args: list, **kwargs: dict):
        ''' define '''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
