import unittest
from http import HTTPStatus
from unittest.mock import patch, MagicMock
from flaskr.service.AuthService import AuthService
from flaskr.models.auth import Auth
from config import Config
import jwt
import datetime
from tests.builder import AuthBuilder
from faker import Faker
from builder import FindIssueBuilder
class AuthServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.user_builder= AuthBuilder()
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
    
    @patch('requests.get')
    def test_return_a_list_of_users_for_pagination(self, get_mock):
        fake = Faker()
        role_id = fake.uuid4()
        users = []
        user =  self.user_builder.build()
        users.append(user)
        users_mock = FindIssueBuilder().with_data(users).build()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = users_mock
        expected_response = {
            'hasNext': users_mock['has_next'],
            'totalPages': users_mock['total_pages'],
            'page': users_mock['page'],
            'limit': users_mock['limit'],
            'data': []
        }

        for user in users_mock['data']:
            expected_response['data'].append({
                "id": user['id'],
                "name": user['name'],
                "last_name": user['last_name'],
                "phone_number": user['phone_number'],
                "email": user['email'],
                "address": user['address'],
                "birthdate": user['birthdate'],
                "role_id": user['role_id']
            })

        response = self.auth_service.get_users_by_role(role_id=role_id,page=1, limit=10)

        self.assertEqual(response, expected_response)
