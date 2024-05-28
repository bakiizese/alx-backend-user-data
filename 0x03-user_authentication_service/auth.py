#!/usr/bin/env python3
''' authentication '''
import bcrypt


def _hash_password(password: str) -> str:
    ''' hash password by bcrypt '''
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
