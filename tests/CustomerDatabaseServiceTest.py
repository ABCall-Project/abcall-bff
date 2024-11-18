import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
import os
from flaskr.service.CustomerDatabaseService import CustomerDatabaseService

class CustomerDatabaseServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['CUSTOMER_API_PATH'] = 'http://fakeurl.com'
        self.service = CustomerDatabaseService()
        self.customer_id = UUID("845eb227-5356-4169-9799-95a97ec5ce33")
        self.entries = [
            {"topic": "Test Topic 1", "content": "Test Content 1"},
            {"topic": "Test Topic 2", "content": "Test Content 2"}
        ]

    @patch('flaskr.service.CustomerDatabaseService.requests.post')
    def test_load_entries_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "Entries loaded successfully"}
        mock_post.return_value = mock_response

        result = self.service.load_entries(self.customer_id, self.entries)

        self.assertIsNotNone(result)
        self.assertEqual(result, {"message": "Entries loaded successfully"})
        mock_post.assert_called_once_with(
            f'{self.service.base_url}/customer/loadCustomerDataBase',
            json={"customer_id": str(self.customer_id), "entries": self.entries}
        )

    @patch('flaskr.service.CustomerDatabaseService.requests.post')
    def test_load_entries_error_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = self.service.load_entries(self.customer_id, self.entries)

        self.assertIsNone(result)
        mock_post.assert_called_once_with(
            f'{self.service.base_url}/customer/loadCustomerDataBase',
            json={"customer_id": str(self.customer_id), "entries": self.entries}
        )

    @patch('flaskr.service.CustomerDatabaseService.requests.post')
    def test_load_entries_exception(self, mock_post):
        mock_post.side_effect = Exception("API is down")

        result = self.service.load_entries(self.customer_id, self.entries)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
