#!/usr/bin/env python3
''' session db '''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    ''' session db class '''
    def create_session(self, user_id=None):
        ''' create usersession instance '''
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id, session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' returns user_id by session_id in db '''
        usr_id = super().user_id_for_session_id(session_id)
        if usr_id:
            return usr_id
        return None

    def destroy_session(self, request=None):
        ''' destroy session '''
        dl = super().destroy_session(request)
        if dl:
            return True
        return False
