#!/usr/bin/env python3
''' main module for every task '''
import requests


url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    ''' check register user '''
    assert isinstance(email, str)
    assert isinstance(password, str)
    url_1 = url + '/users'
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
    ''' check with wrong password '''
    assert isinstance(email, str)
    assert isinstance(password, str)
    url_1 = url + '/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url_1, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    ''' check log_in '''
    assert isinstance(email, str)
    assert isinstance(password, str)
    url_1 = url + '/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url_1, data=data)
    assert response.status_code == 200
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    ''' unlog to index '''
    url_1 = url + '/profile'
    response = requests.get(url_1)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    ''' log-in profile '''
    assert isinstance(session_id, str)
    url_1 = url + '/profile'
    data = {'session_id': session_id}
    response = requests.get(url_1, cookies=data)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    ''' logout '''
    url_1 = url + '/sessions'
    assert isinstance(session_id, str)
    data = {'session_id': session_id}
    response = requests.delete(url_1, cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    ''' reset token '''
    assert isinstance(email, str)
    url_1 = url + '/reset_password'
    data = {'email': email}

    response = requests.post(url_1, data=data)
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    ''' update pwd '''
    assert isinstance(email, str)
    assert isinstance(new_password, str)
    assert isinstance(reset_token, str)
    url_1 = url + '/reset_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url_1, data=data)
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
