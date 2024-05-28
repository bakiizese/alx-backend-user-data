#!/usr/bin/env python3
''' authentication '''
import bcrypt


def _hash_password(password: str) -> bytes:
    ''' hash password by bcrypt '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
