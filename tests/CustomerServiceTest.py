import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from flaskr.service.CustomerService import CustomerService 


class CustomerServiceTest(unittest.TestCase):

    def setUp(self):
        self.customer_service = CustomerService()
        self.plan_id = UUID("845eb227-5356-4169-9799-95a97ec5ce33")
        self.customers = [
            {"document": "123456789", "name": "John Doe"},
            {"document": "987654321", "name": "Jane Smith"}
        ]

    @patch('service.CustomerService.requests.post')
    def test_add_customers_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "Customers added successfully"}
        mock_post.return_value = mock_response

        result = self.customer_service.add_customers(self.customers, self.plan_id)
        self.assertEqual(result, {"message": "Customers added successfully"})
        mock_post.assert_called_once_with(
            f'{self.customer_service.base_url}/customer/loadCustomers',
            json={"plan_id": str(self.plan_id), "customers": self.customers}
        )

    @patch('service.CustomerService.requests.post')
    def test_add_customers_error_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        result = self.customer_service.add_customers(self.customers, self.plan_id)
        self.assertIsNone(result)
        mock_post.assert_called_once_with(
            f'{self.customer_service.base_url}/customer/loadCustomers',
            json={"plan_id": str(self.plan_id), "customers": self.customers}
        )

    @patch('service.CustomerService.requests.post')
    def test_add_customers_exception(self, mock_post):
        mock_post.side_effect = Exception("API is down")

        result = self.customer_service.add_customers(self.customers, self.plan_id)
        self.assertIsNone(result)