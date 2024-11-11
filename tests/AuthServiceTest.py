import unittest
from unittest.mock import patch, MagicMock
from flaskr.service.AuthService import AuthService
from flaskr.models.auth import Auth
from config import Config
import jwt
import datetime

class AuthServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.auth_service = AuthService()
        self.email = "test@example.com"
        self.password = "password123"
        self.mock_user_data = {
            "id": "1234",
            "name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "email": self.email,
            "address": "123 Main St",
            "birthdate": "1990-01-01",
            "role_id": "admin"
        }

   

    @patch('flaskr.service.AuthService.requests.post')
    def test_autenticate_no_user_found(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = None

        result = self.auth_service.autenticate(self.email, self.password)
        self.assertIsNone(result)

    @patch('flaskr.service.AuthService.requests.post')
    def test_autenticate_invalid_credentials(self, mock_post):
        mock_post.return_value.status_code = 401

        result = self.auth_service.autenticate(self.email, self.password)
        self.assertIsNone(result)

    @patch('flaskr.service.AuthService.requests.post')
    def test_autenticate_api_error(self, mock_post):
        mock_post.return_value.status_code = 500

        result = self.auth_service.autenticate(self.email, self.password)
        self.assertIsNone(result)

    @patch('flaskr.service.AuthService.requests.post')
    def test_autenticate_exception(self, mock_post):
        mock_post.side_effect = Exception("API is down")

        result = self.auth_service.autenticate(self.email, self.password)
        self.assertIsNone(result)
