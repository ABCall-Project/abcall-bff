from functools import wraps
from http import HTTPStatus
import uuid
import re
from flask import request, jsonify
from datetime import datetime

def validate_customer_user():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            name = data.get('name')
            last_name = data.get('last_name') if data.get('last_name') else ''
            phone_number = data.get('phone_number') if data.get('phone_number') else ''
            email = data.get('email')
            address = data.get('address') if data.get('address') else ''
            birthdate = data.get('birthdate') if data.get('birthdate') else ''
            password = data.get('password')
            document = data.get('document')
            plan_id = data.get('plan_id')

            if not name or name == "":
                return {"message": "Name cannot be empty"}, HTTPStatus.BAD_REQUEST
            
            if not password or password == "":
                return {"message": "Password cannot be empty"}, HTTPStatus.BAD_REQUEST
            
            if not email or email == "":
                return {"message": "Email cannot be empty"}, HTTPStatus.BAD_REQUEST
            
            if len(name) > 50:
                return {"message": "The Name is not complete with the maximum, should be 50 characters"}, HTTPStatus.BAD_REQUEST
            
            if len(last_name) > 50:
                return {"message": "The Last name is not complete with the maximum, should be 50 characters"}, HTTPStatus.BAD_REQUEST
            
            if len(phone_number) > 10:
                return {"message": "The phone number is not complete with the maximum, should be 10 characters"}, HTTPStatus.BAD_REQUEST
            
            if len(email) > 100:
                return {"message": "The email is not complete with the maximum, should be 100 characters"}, HTTPStatus.BAD_REQUEST
            
            if len(address) > 255:
                return {"message": "The address is not complete with the maximum, should be 255 characters"}, HTTPStatus.BAD_REQUEST
            
            if not re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):
                return {"message": "The email should be a valid email example@mail.com"}, HTTPStatus.BAD_REQUEST
            
            if birthdate != '' and not validate_date(birthdate):
                return jsonify({"message": "The birthdate should be a date format"}), HTTPStatus.BAD_REQUEST
                  
            if document != None and len(document) > 20:
                return {"message": "The Document is not complete with the maximum, should be 20 characters"}, HTTPStatus.BAD_REQUEST
            
            if plan_id != None and not is_valid_uuid(plan_id):
                return jsonify({"message": "It is not a valid plan id with an uuid format"}), HTTPStatus.BAD_REQUEST

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
    
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False