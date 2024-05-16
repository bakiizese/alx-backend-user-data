#!/usr/bin/env python3
''' pasword ecnryption '''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' password hashed '''
    encod = password.encode()
    hashs = bcrypt.hashpw(encod, bcrypt.gensalt())

    return hashs


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' check validation '''
    vd = False
    encod = password.encode()
    if bcrypt.checkpw(encod, hashed_password):
        vd = True
    return vd
