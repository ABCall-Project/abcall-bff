from functools import wraps
import jwt
from flask import request, jsonify
from config import Config
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if os.getenv('FLASK_ENV') == 'test':
            return f(*args, **kwargs)
        
        config = Config()
        token = request.headers.get('Authorization')
        
        
        if not token:
           return {"message": "Token es requerido"}, 403

        try:
            token=str(token).replace('Bearer ','')
            data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
            current_user = data["user"]
        except jwt.ExpiredSignatureError:
            return {"message": "expired token"}, 403
        except jwt.InvalidTokenError:
            return {"message": "invalid token"}, 403

        return f(*args, **kwargs)
    return decorated
