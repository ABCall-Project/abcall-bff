import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from CustomerDatabaseService import CustomerDatabaseService


class CustomerDatabaseServiceTest(unittest.TestCase):
    
    @patch('CustomerDatabaseService.requests.post')
    @patch('CustomerDatabaseService.os.environ.get', return_value='http://mock-api')
    def test_load_entries_success(self, mock_env, mock_post):
        """
        Test successful entry loading into the customer database.
        """
        # Arrange
        service = CustomerDatabaseService()
        customer_id = UUID('12345678-1234-5678-1234-567812345678')
        entries = [
            {"topic": "TestTopic1", "content": "TestContent1"},
            {"topic": "TestTopic2", "content": "TestContent2"}
        ]
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"message": "Entries loaded successfully"}
        mock_post.return_value = mock_response

        # Act
        result = service.load_entries(customer_id, entries)

        # Assert
        mock_post.assert_called_once_with(
            'http://mock-api/customer/loadCustomerDataBase',
            json={"customer_id": str(customer_id), "entries": entries}
        )
        self.assertEqual(result, {"message": "Entries loaded successfully"})

    @patch('CustomerDatabaseService.requests.post')
    @patch('CustomerDatabaseService.os.environ.get', return_value='http://mock-api')
    def test_load_entries_error_response(self, mock_env, mock_post):
        """
        Test handling of an error response from the API.
        """
        # Arrange
        service = CustomerDatabaseService()
        customer_id = UUID('12345678-1234-5678-1234-567812345678')
        entries = [
            {"topic": "TestTopic1", "content": "TestContent1"}
        ]
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Act
        result = service.load_entries(customer_id, entries)

        # Assert
        mock_post.assert_called_once_with(
            'http://mock-api/customer/loadCustomerDataBase',
            json={"customer_id": str(customer_id), "entries": entries}
        )
        self.assertIsNone(result)

    @patch('CustomerDatabaseService.requests.post', side_effect=Exception("Network error"))
    @patch('CustomerDatabaseService.os.environ.get', return_value='http://mock-api')
    def test_load_entries_exception(self, mock_env, mock_post):
        """
        Test handling of an exception during the API call.
        """
        # Arrange
        service = CustomerDatabaseService()
        customer_id = UUID('12345678-1234-5678-1234-567812345678')
        entries = [
            {"topic": "TestTopic1", "content": "TestContent1"}
        ]

        # Act
        result = service.load_entries(customer_id, entries)

        # Assert
        mock_post.assert_called_once_with(
            'http://mock-api/customer/loadCustomerDataBase',
            json={"customer_id": str(customer_id), "entries": entries}
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
