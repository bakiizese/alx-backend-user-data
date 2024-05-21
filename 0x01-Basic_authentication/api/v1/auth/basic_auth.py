#!/usr/bin/env python3
''' basic auth class '''
from api.v1.auth.auth import Auth
import base64


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
            baseutf = base.decode('utf-8')
        except Exception:
            return None

        return baseutf

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
