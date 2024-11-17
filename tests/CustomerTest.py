import unittest
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from uuid import uuid4
from flaskr.app import app

class CustomerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')  # Ruta corregida
    def test_post_add_customers_success(self, add_customers_mock):
        fake_plan_id = str(uuid4())
        fake_customers = [
            {"document": "123456789", "name": "John Doe"},
            {"document": "987654321", "name": "Jane Smith"}
        ]
        mock_response = [
            {"id": str(uuid4()), "document": "123456789", "name": "John Doe"},
            {"id": str(uuid4()), "document": "987654321", "name": "Jane Smith"}
        ]
        add_customers_mock.return_value = mock_response

        response = self.client.post(
            '/customer/loadCustomers',
            json={"plan_id": fake_plan_id, "customers": fake_customers}
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json, mock_response)

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')  # Ruta corregida
    def test_post_add_customers_failure(self, add_customers_mock):
        fake_plan_id = str(uuid4())
        fake_customers = [{"document": "123456789", "name": "John Doe"}]
        add_customers_mock.return_value = None

        response = self.client.post(
            '/customer/loadCustomers',
            json={"plan_id": fake_plan_id, "customers": fake_customers}
        )

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json, {"message": "Failed to add customers"})

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')  # Ruta corregida
    def test_post_add_customers_invalid_request(self, add_customers_mock):
        fake_customers = [{"document": "123456789", "name": "John Doe"}]

        response = self.client.post(
            '/customer/loadCustomers',
            json={"customers": fake_customers}  # Missing plan_id
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("message", response.json)

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')  # Ruta corregida
    def test_post_add_customers_exception(self, add_customers_mock):
        fake_plan_id = str(uuid4())
        fake_customers = [{"document": "123456789", "name": "John Doe"}]
        add_customers_mock.side_effect = Exception("Some unexpected error")

        response = self.client.post(
            '/customer/loadCustomers',
            json={"plan_id": fake_plan_id, "customers": fake_customers}
        )

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json, {'message': 'An error occurred while adding customers'})
