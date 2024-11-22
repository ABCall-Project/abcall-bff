from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from http import HTTPStatus
from ...service.AuthService import AuthService
import logging

from config import Config
from ...middleware.AuthMiddleware import token_required
from flaskr.models.Role import Role
from flaskr.models.CustomerUser import CustomerUser



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
        if action == 'signup':
            return self.sign_up()
        else:
            return {"message": "Action not found"}, 404
        
    def sign_up(self):
        self.logger.info('receiving request to signup')
        try:
            if request.is_json:  
                data = request.get_json()
                email = data.get('email')
                password = data.get('password')
                name = data.get('name')
                last_name = data.get('last_name')
                phone_number = data.get('phone_number')
                address = data.get('address')
                birthdate = data.get('birthdate')
                role_id = Role.COMPANY_ADMIN.value
                document = data.get('document')
                plan_id = data.get('plan_id')
                self.logger.info(f'Receive request to signup {email}')

                customer_user = CustomerUser(email=email, \
                                             password=password, \
                                             name=name, last_name=last_name, \
                                             phone_number=phone_number, \
                                             address=address, \
                                             birthdate=birthdate, \
                                             role_id=role_id, \
                                             document=document, \
                                             plan_id=plan_id, \
                                             )

                user = self.service.create_user(customer_user)
                if user:
                    return {
                        'message': user['message']
                    }, HTTPStatus.CREATED
                else:
                    return None, HTTPStatus.CONFLICT
            else:
                return None, HTTPStatus.BAD_REQUEST
        
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to signup: {ex}')
            return {'message': 'Something was wrong trying to create user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        


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
    