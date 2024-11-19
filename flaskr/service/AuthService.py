from datetime import date
from typing import Optional
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
from uuid import UUID
import requests
import re
import os
import logging
from ..models.auth import Auth
from config import Config
import jwt
import datetime

class AuthService:
    """
    This class is for integrate the bff with the Auth service
    Attributes:
        base_url (string): the Auth api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        self.config=Config()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instancing auth service')
        self.base_url = self.config.AUTH_API_PATH   
    
    def authenticate(self,email,password):
        """
        method to authenticate a user
        Args:
            email (str): email account
            password (str): password account
        Return:
            user (Auth): user with jwt token
        """
        user=None
        try:
            self.logger.info(f'init consuming api user {self.base_url}')
            data = {
                "email": email,
                "password": password
            }
            response = requests.post(f'{self.base_url}/users/getUserByCredentials',json=data)
            self.logger.info('quering auth')
            if response.status_code == 200:
                self.logger.info('status code 200 auth')
                data = response.json()
                if data:
                    self.logger.info('there are auth response ')

                    user=Auth(
                        data.get('id'),
                        data.get('name'),
                        data.get('last_name'),
                        data.get('phone_number'),
                        data.get('email'),
                        data.get('address'),
                        data.get('birthdate'),
                        data.get('role_id'),
                        '',
                        data.get('customer_id')
                    )
                    self.logger.info('user authenticated, generating token')
                    user.token = jwt.encode(
                        {
                            "user": email,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=int(self.config.HOURS_TO_EXPIRE_SESSION))
                        },
                        self.config.SECRET_KEY,
                        algorithm="HS256"
                    )
                    self.logger.info(f'user to response {user.to_dict()}')
                    return user
                else:
                    self.logger.info('there arent response')
                    return None
            else:
                self.logger.info(f"error consuming auth: {response.status_code}")
                return None
        except Exception as e:
            self.logger.info(f"Error comunication with auth: {str(e)}")
            return None
        
    def get_users_by_role(self,role_id:UUID,page:int,limit:int):
        try:
            
            self.logger.info(f'init consuming api getUsersByRole details {self.base_url}/users/getUsersByRole?role_id=${role_id}&page=${page}&limit=${limit}')
            response = requests.get(f'{self.base_url}/users/getUsersByRole?role_id={role_id}&page={page}&limit={limit}')
            self.logger.info(f'quering getUsersByRole details by getUsersByRole id')
            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error querying Users service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with users service: {str(e)}')
            raise e