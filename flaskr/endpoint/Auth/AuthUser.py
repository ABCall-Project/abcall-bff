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
        if action == 'getUsersByRole':
            return self.get_users_by_role()
        else:
            return {"message": "Action not found"}, 404
        
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
                user = self.service.authenticate(email,password)
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
    
    def get_users_by_role(self):
        try:
            self.logger.info('Receive request to get get_users_by_role')
            role_id = request.args.get('role_id')
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))

            users_paginated = self.service.get_users_by_role(role_id=role_id,page=page,limit=limit)
            if users_paginated:
                return users_paginated, HTTPStatus.OK
            
            return {}, HTTPStatus.NOT_FOUND
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to get_users_by_role {ex}')
            return {'message': 'Something was wrong trying to get_users_by_role'}, HTTPStatus.INTERNAL_SERVER_ERROR
    