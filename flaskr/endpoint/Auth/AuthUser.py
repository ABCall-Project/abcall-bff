from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from http import HTTPStatus
from ...service.AuthService import AuthService
import logging

from config import Config
from ...middleware.AuthMiddleware import token_required



class AuthUser(Resource):

    def __init__(self):
        config = Config()
        self.service = AuthService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')

    @token_required
    def get(self, action=None):
        return {"message":"test protected path ok"},HTTPStatus.OK


   
        
    def post(self, action=None):
        if action == 'signin':
            return self.sign_in()
        else:
            return {"message": "Action not found"}, 404
        
    
    def sign_in(self):
        self.logger.info('receiving request to signin')
        try:

            if request.is_json:  
                data = request.get_json()
                email = data.get('email')
                password = data.get('password')
                self.logger.info(f'Receive request to signin {email}')
                user = self.service.autenticate(email,password)
                if user:
                    user_s=user.to_dict()
                    return user_s, HTTPStatus.OK
                else:
                    return None, HTTPStatus.UNAUTHORIZED
            else:
                return None, HTTPStatus.UNAUTHORIZED
        
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to signin: {ex}')
            return {'message': 'Something was wrong trying to get user by credentials'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    