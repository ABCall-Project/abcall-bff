import unittest
from unittest.mock import Mock, MagicMock, patch
from http import HTTPStatus
from faker import Faker
from flaskr.app import app
from builder import AuthBuilder, CustomerUserRequestBuilder, CustomerCreationResponseBuilder
from flaskr.service.AuthService import AuthService
from flaskr.service.CustomerService import CustomerService

class AuthUserTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock(spec=AuthService)
        self.mock_customer_service = MagicMock(spec=CustomerService)
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

    @patch('flaskr.service.AuthService.requests.post')
    def test_should_sign_up_a_new_user(self, mock_post):
        data = CustomerUserRequestBuilder().build()
        customer_response = CustomerCreationResponseBuilder() \
                            .with_name(data['name']) \
                            .with_plan_id(data['plan_id']) \
                            .build()
        response_mock = {
            "message": "User created successfully"
        }
        mock_post.side_effect = [
            MagicMock(status_code=HTTPStatus.CREATED, json=MagicMock(return_value=customer_response)),
            MagicMock(status_code=HTTPStatus.OK, json=MagicMock(return_value=response_mock))
        ]
        
        response = self.client.post('/auth/signup', json=data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json['message'], response_mock['message'])
    
    @patch('flaskr.service.AuthService.requests.post')
    def test_should_return_internal_server_error_when_something_is_wrong_on_customer_creation(self, mock_post):
        data = CustomerUserRequestBuilder().build()
        mock_post.side_effect = [
            MagicMock(status_code=HTTPStatus.CONFLICT, json=MagicMock(return_value=None))
        ]
        
        response = self.client.post('/auth/signup', json=data)

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json, None)
    
    @patch('flaskr.service.AuthService.requests.post')
    def test_should_return_conflict_when_user_exist(self, mock_post):
        data = CustomerUserRequestBuilder().build()
        customer_response = CustomerCreationResponseBuilder() \
                    .with_name(data['name']) \
                    .with_plan_id(data['plan_id']) \
                    .build()
        mock_post.side_effect = [
            MagicMock(status_code=HTTPStatus.CREATED, json=MagicMock(return_value=customer_response)),
            MagicMock(status_code=HTTPStatus.CONFLICT, json=MagicMock(return_value=None))
        ]
        
        response = self.client.post('/auth/signup', json=data)

        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertEqual(response.json, None)

    @patch('flaskr.service.AuthService.requests.post')
    def test_should_return_bad_request_is_the_request_has_an_invalid_format(self, mock_post):
        data = CustomerUserRequestBuilder().build()
        customer_response = CustomerCreationResponseBuilder() \
                    .with_name(data['name']) \
                    .with_plan_id(data['plan_id']) \
                    .build()
        mock_post.side_effect = [
            MagicMock(status_code=HTTPStatus.CREATED, json=MagicMock(return_value=customer_response)),
            MagicMock(status_code=HTTPStatus.CONFLICT, json=MagicMock(return_value=None))
        ]
        
        response = self.client.post('/auth/signup', data=data)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, None)