#!/usr/bin/env python3
''' session db '''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    ''' session db class '''
    def create_session(self, user_id=None):
        ''' create usersession instance '''
        session_id = super().create_session(user_id)
        if session_id:
            kwarg = {'user_id': user_id, 'session_id': session_id}
            user_session = UserSession(**kwarg)
            user_session.save()
            user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' returns user_id by session_id in db '''
        if not session_id:
            return None
        UserSession.load_from_file()
        g = UserSession.search({'session_id': session_id})
        if not g:
            return None
        g = g[0]
        dur = timedelta(seconds=self.session_duration)
        time = g.created_at + dur
        if time < datetime.now():
            return None
        return g.user_id

    def destroy_session(self, request=None):
        ''' destroy session '''
        if request:
            check = self.session_cookie(request)
            if check:
                to_del = UserSession.search({'session_id': check})
                if to_del:
                    dels = to_del[0]
                    dels.remove()
                    UserSession.save_to_file()
                    return True
        return False
