#!/usr/bin/env python3
''' flask app '''
from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/session', methods=['DELETE'], strict_slashes=False)
def logout():
    ''' logout '''
    session = request.get_cookie('session_id')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
