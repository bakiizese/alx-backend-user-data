#!/usr/bin/env python3
''' main module for every task '''
import requests


url = "http://192.168.1.4:5000/"

def register_user(email: str, password: str) -> None:
    ''' check register user '''
    url_1 = url + 'users'
    data = {
        'email': email,
        'password': password
    }
    r = {"email": email, "message": "user created"}
    r2 = {"message": "email already registered"}
    response = requests.post(url_1, data=data)
    assert response.json() == r
    assert response.status_code == 200
    response = requests.post(url_1, data=data)
    assert response.status_code == 400
    assert response.json() == r2

def log_in_wrong_password(email: str, password: str) -> None:
    pass

def log_in(email: str, password: str) -> str:
    pass

def profile_unlogged() -> None:
    pass

def profile_logged(session_id: str) -> None:
    pass

def log_out(session_id: str) -> None:
    pass

def reset_password_token(email: str) -> str:
    pass

def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    #log_in_wrong_password(EMAIL, NEW_PASSWD)
    #profile_unlogged()
    #session_id = log_in(EMAIL, PASSWD)
    #profile_logged(session_id)
    #log_out(session_id)
    #reset_token = reset_password_token(EMAIL)
    #update_password(EMAIL, reset_token, NEW_PASSWD)
    #log_in(EMAIL, NEW_PASSWD)
