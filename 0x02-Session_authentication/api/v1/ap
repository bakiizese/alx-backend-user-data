#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from flask_login import current_user
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = getenv('AUTH_TYPE', None)

if auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()
elif auth is not None:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def un_auth(error) -> str:
    ''' handle un-auth '''
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    ''' forbidden '''
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    ''' run befo evry func '''
    global auth
    if auth:
        if auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/',
                                            '/api/v1/auth_session/login/']):
            if (
                    not auth.authorization_header(request) and
                    not auth.session_cookie(request)):
                return abort(401)
            if not auth.current_user(request):
                return abort(403)
            request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=1)
