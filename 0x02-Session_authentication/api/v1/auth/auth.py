#!/usr/bin/env python3
''' auth class '''
from typing import List, TypeVar
from os import getenv

session_name = getenv('SESSION_NAME', None)


class Auth:
    ''' class auth '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' return bool '''
        path1 = ''
        if not path or not excluded_paths:
            return True
        if path[-1] == '/':
            path1 = path[:-1]
        else:
            path1 = path + '/'
        for ls in excluded_paths:
            if ls[-1] == '*':
                ls = ls[:-1]
            if ls in path1 or ls in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' return None for now '''
        if not request:
            return None
        auth_header = request.headers
        if 'Authorization' in auth_header:
            auth_h = auth_header.get('Authorization')
            return auth_h
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' returns None for now '''
        return None

    def session_cookie(self, request=None):
        ''' return cookies '''
        if not request or not session_name:
            return None
        rt = request.cookies.get(session_name)

        return rt
