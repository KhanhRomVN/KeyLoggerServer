from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        # Add your admin verification logic here
        # For now, we'll just allow any authenticated user
        return fn(*args, **kwargs)
    return wrapper

def client_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # Add client-specific verification logic if needed
        return fn(*args, **kwargs)
    return wrapper