#!/usr/bin/env python3
''' session auth '''
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    ''' session auth '''
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        ''' assign session id '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' search by session id '''
        if not session_id or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        ''' return user id by session id '''
        cookie = self.session_cookie(request)
        cook = self.user_id_for_session_id(cookie)
        if cook:
            return User.get(cook)
        return None
