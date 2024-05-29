#!/usr/bin/env python3
''' flask app '''
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
