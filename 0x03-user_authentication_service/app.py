#!/usr/bin/env python3
''' flask app '''
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    ''' index route '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    '''register user'''
    em = request.form.get('email')
    ps = request.form.get('password')

    try:
        usr = AUTH.register_user(em, ps)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{em}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def session():
    ''' create session '''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session = AUTH.create_session(email)
        if session:
            response = make_response({"email": f"{email}",
                                     "message": "logged in"})
            response.set_cookie('session_id', session)
            return response
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' logout '''
    session = request.cookies.get('session_id')
    if not session:
        abort(403)
    usr = AUTH.get_user_from_session_id(session)
    if usr:
        AUTH.destroy_session(usr.id)
        response = make_response(redirect('/'))
        response.delete_cookie('session_id')
        return response
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    ''' find user by session '''
    session = request.cookies.get('session_id')
    if not session:
        abort(403)
    usr = AUTH.get_user_from_session_id(session)
    if usr:
        return jsonify({"email": f"{usr.email}"}), 200
    abort(403)


@app.route('/reset_password',  methods=['POST'], strict_slashes=False)
def reset_password():
    ''' reset tk by email '''
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        usr = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{usr}"}), 200


@app.route('/reset_password',  methods=['PUT'], strict_slashes=False)
def reset_pwd():
    ''' reset ps by token '''
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email,
                    "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
