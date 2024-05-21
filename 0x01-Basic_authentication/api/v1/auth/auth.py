#!/usr/bin/env python3
''' auth class '''
from flask import request
from typing import List, TypeVar


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
        if path1 in excluded_paths or path in excluded_paths:
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
