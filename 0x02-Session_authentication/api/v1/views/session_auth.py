#!/usr/bin/env python3
''' session auth '''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models.user import User
from api.v1.app import auth
from os import getenv

sess_name = getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_sess():
    ''' route to auth session'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    dicts = {'email': email}
    if not User.search(dicts):
        return jsonify({"error": "no user found for this email"}), 404

    based_on_email = User.search(dicts)
    based_on_email = based_on_email[0]
    if not based_on_email.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    dicts['password'] = based_on_email.password
    search_based_em_pwd = User.search(dicts)
    usr = search_based_em_pwd[0]
    from api.v1.app import auth
    cookie_of_usr = auth.create_session(usr.id)
    response = make_response(usr.to_json())
    response.set_cookie(sess_name, cookie_of_usr)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_logout():
    ''' route to logout '''
    if not auth.destroy_session(request):
        abort(404)
    return {}, 200
