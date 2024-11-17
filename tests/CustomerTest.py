import unittest
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from uuid import uuid4
from flaskr.app import app

class CustomerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')
    def test_post_add_customers_success(self, add_customers_mock):
        fake_plan_id = str(uuid4())
        fake_customers = [{"document": "123456789", "name": "John Doe"}, {"document": "987654321", "name": "Jane Smith"}]
        add_customers_mock.return_value = [
            {"id": str(uuid4()), "document": "123456789", "name": "John Doe"},
            {"id": str(uuid4()), "document": "987654321", "name": "Jane Smith"}
        ]

        response = self.client.post('/customer/addCustomers', json={"plan_id": fake_plan_id, "customers": fake_customers})

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    @patch('flaskr.service.CustomerService.CustomerService.add_customers')
    def test_post_add_customers_failure(self, add_customers_mock):
        fake_plan_id = str(uuid4())
        fake_customers = [{"document": "123456789", "name": "John Doe"}]
        add_customers_mock.return_value = None

        response = self.client.post('/customer/addCustomers', json={"plan_id": fake_plan_id, "customers": fake_customers})

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
