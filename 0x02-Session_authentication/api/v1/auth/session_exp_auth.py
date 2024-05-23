#!/usr/bin/env python3
''' expiration of sessions '''
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv

duration = getenv('SESSION_DURATION', 0)

try:
    duration = int(duration)
except Exception:
    duration = 0


class SessionExpAuth(SessionAuth):
    ''' expire session '''
    def __init__(self):
        ''' define duration of exp '''
        self.session_duration = duration

    def create_session(self, user_id=None):
        ''' super() '''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' check exp '''
        if not session_id:
            return None
        try:
            self.user_id_by_session_id[session_id]
        except Exception:
            return None

        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']

        try:
            self.user_id_by_session_id[session_id]['created_at']:
        except Exception:
            return None

        created_at = self.user_id_by_session_id[session_id]['created_at']
        dur = timedelta(seconds=self.session_duration)
        if created_at + dur < datetime.now():
            return None
        return self.user_id_by_session_id[session_id]['user_id']
