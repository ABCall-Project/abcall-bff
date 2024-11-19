import unittest
from unittest.mock import Mock, MagicMock, patch
from http import HTTPStatus
from faker import Faker
from flaskr.app import app
from builder import AuthBuilder
from flaskr.service.AuthService import AuthService

class AuthUserTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock(spec=AuthService)
        self.client = app.test_client()

    @patch('flaskr.service.AuthService.requests.post')
    def test_should_sign_in_user(self, mock_post):
        fake = Faker()
        data = {
            'email': fake.email(),
            'password': fake.password()
        }
        auth = AuthBuilder().with_email(data['email']) \
                .build()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = auth
        mock_post.return_value = mock_response
        
        response = self.client.post('/auth/signin', json=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json['email'], data['email'])