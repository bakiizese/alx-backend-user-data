#!/usr/bin/env python3
''' basic auth class '''
from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import Base
from typing import TypeVar


class BasicAuth(Auth):
    ''' class '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        ''' check if can be encode '''
        if not authorization_header or not isinstance(authorization_header,
                                                      str):
            return None

        ls = authorization_header.split(' ')

        if ls[0] != 'Basic':
            return None
        auths = str(ls[1])
        return auths

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        ''' decode to base64 '''
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base = base64.b64decode(base64_authorization_header)
        except Exception:
            print('her')
            return None

        baseutf = base.decode('utf-8')
        return base

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        ''' return tuple '''
        if (
                not decoded_base64_authorization_header or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return (None, None)
        sp = decoded_base64_authorization_header.split(':')
        return (sp[0], sp[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        ''' get user '''
        if (
                not user_email or not user_pwd or
                not isinstance(user_email, str) or
                not isinstance(user_pwd, str)
                ):
            return None

        try:
            User.all()
        except Exception:
            return None
        dicts = {'email': user_email}
        if not User.search(dicts):
            return None

        based_on_email = User.search(dicts)
        based_on_email = based_on_email[0]
        if based_on_email.is_valid_password(user_pwd):
            dicts['password'] = based_on_email.password
            search_based_em_pwd = User.search(dicts)
            return search_based_em_pwd[0]
        return None
