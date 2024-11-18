import unittest
from unittest.mock import patch, MagicMock
import os
from flaskr.service.CustomerService import CustomerService

class CustomerServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['CUSTOMER_API_PATH'] = 'http://fakeurl.com'
        self.service = CustomerService()

    @patch('flaskr.service.CustomerService.requests.post')
    def test_add_customers_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'message': 'Customers added successfully'}
        mock_post.return_value = mock_response

        customers = [
            {"document": "123456789", "name": "John Doe"},
            {"document": "987654321", "name": "Jane Smith"}
        ]
        plan_id = '845eb227-5356-4169-9799-95a97ec5ce33'

        result = self.service.add_customers(customers, plan_id)

        self.assertIsNotNone(result)
        self.assertEqual(result, {'message': 'Customers added successfully'})
        mock_post.assert_called_once_with(
            f'{self.service.base_url}/customer/loadCustomers',
            json={"plan_id": plan_id, "customers": customers}
        )

    @patch('flaskr.service.CustomerService.requests.post')
    def test_add_customers_error_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        customers = [
            {"document": "123456789", "name": "John Doe"}
        ]
        plan_id = '845eb227-5356-4169-9799-95a97ec5ce33'

        result = self.service.add_customers(customers, plan_id)

        self.assertIsNone(result)
        mock_post.assert_called_once_with(
            f'{self.service.base_url}/customer/loadCustomers',
            json={"plan_id": plan_id, "customers": customers}
        )

    @patch('flaskr.service.CustomerService.requests.post')
    def test_add_customers_exception(self, mock_post):
        mock_post.side_effect = Exception("API is down")

        customers = [
            {"document": "123456789", "name": "John Doe"}
        ]
        plan_id = '845eb227-5356-4169-9799-95a97ec5ce33'

        result = self.service.add_customers(customers, plan_id)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
