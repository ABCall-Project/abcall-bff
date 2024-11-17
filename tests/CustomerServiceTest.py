import unittest
from unittest.mock import patch, MagicMock
import os
from flaskr.service.CustomerService import CustomerService
from uuid import uuid4

class CustomerServiceTest(unittest.TestCase):

    def setUp(self):
        os.environ['CUSTOMER_API_PATH'] = 'http://fakeurl.com'
        self.service = CustomerService()

    @patch('requests.post')
    def test_add_customers_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = [
            {"id": str(uuid4()), "document": "987654321", "name": "John Doe"},
            {"id": str(uuid4()), "document": "123456789", "name": "Jane Smith"}
        ]
        mock_post.return_value = mock_response

        customers = [{"document": "987654321", "name": "John Doe"}, {"document": "123456789", "name": "Jane Smith"}]
        plan_id = str(uuid4())
        result = self.service.add_customers(customers, plan_id)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    @patch('requests.post')
    def test_add_customers_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        customers = [{"document": "987654321", "name": "John Doe"}]
        plan_id = str(uuid4())
        result = self.service.add_customers(customers, plan_id)

        self.assertIsNone(result)

    @patch('requests.post')
    def test_add_customers_exception(self, mock_post):
        mock_post.side_effect = Exception("Some error occurred")

        customers = [{"document": "987654321", "name": "John Doe"}]
        plan_id = str(uuid4())
        result = self.service.add_customers(customers, plan_id)

        self.assertIsNone(result)
