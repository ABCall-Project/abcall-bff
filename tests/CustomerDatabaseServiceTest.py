import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID
from flaskr.service.CustomerDatabaseService import CustomerDatabaseService


class CustomerDatabaseServiceTest(unittest.TestCase):
    
    @patch('requests.post')
    @patch('os.environ.get', return_value='http://mock-api')
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

    @patch('requests.post')
    @patch('os.environ.get', return_value='http://mock-api')
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
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        # Act
        result = service.load_entries(customer_id, entries)

        # Assert
        mock_post.assert_called_once_with(
            'http://mock-api/customer/loadCustomerDataBase',
            json={"customer_id": str(customer_id), "entries": entries}
        )
        self.assertIsNone(result)

    @patch('requests.post', side_effect=Exception("Network error"))
    @patch('os.environ.get', return_value='http://mock-api')
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

    @patch('requests.post')
    def test_create_issue_success(self, mock_post):
        """
        Test successful creation of an issue.
        """
        # Arrange
        url = f'{self.issue_service.base_url}/issue/post'
        auth_user_id = "12345678-1234-5678-1234-567812345678"
        auth_user_agent_id = "87654321-4321-8765-4321-876543218765"
        subject = "Test Issue"
        description = "This is a test issue description."
        mock_response = MagicMock(status_code=HTTPStatus.CREATED)
        mock_response.json.return_value = {
            "id": "09876543-2109-8765-4321-098765432109",
            "auth_user_id": auth_user_id,
            "auth_user_agent_id": auth_user_agent_id,
            "subject": subject,
            "description": description
        }
        mock_post.return_value = mock_response

        # Act
        result = self.issue_service.create_issue(auth_user_id, auth_user_agent_id, subject, description)

        # Assert
        self.assertEqual(result, mock_response.json())
        mock_post.assert_called_once_with(
            url,
            data={
                "auth_user_id": auth_user_id,
                "auth_user_agent_id": auth_user_agent_id,
                "subject": subject,
                "description": description,
            },
            files=None
        )

    @patch('requests.post')
    def test_create_issue_failure(self, mock_post):
        """
        Test failure to create an issue when the API returns a non-201 status code.
        """
        # Arrange
        url = f'{self.issue_service.base_url}/issue/post'
        auth_user_id = "12345678-1234-5678-1234-567812345678"
        auth_user_agent_id = "87654321-4321-8765-4321-876543218765"
        subject = "Test Issue"
        description = "This is a test issue description."
        mock_response = MagicMock(status_code=HTTPStatus.BAD_REQUEST)
        mock_response.text = "Invalid request"
        mock_post.return_value = mock_response

        # Act
        result = self.issue_service.create_issue(auth_user_id, auth_user_agent_id, subject, description)

        # Assert
        self.assertIsNone(result)
        mock_post.assert_called_once_with(
            url,
            data={
                "auth_user_id": auth_user_id,
                "auth_user_agent_id": auth_user_agent_id,
                "subject": subject,
                "description": description,
            },
            files=None
        )

    @patch('requests.post')
    def test_create_issue_exception(self, mock_post):
        """
        Test handling of exceptions during issue creation.
        """
        # Arrange
        url = f'{self.issue_service.base_url}/issue/post'
        auth_user_id = "12345678-1234-5678-1234-567812345678"
        auth_user_agent_id = "87654321-4321-8765-4321-876543218765"
        subject = "Test Issue"
        description = "This is a test issue description."
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        # Act & Assert
        with self.assertRaises(requests.exceptions.RequestException):
            self.issue_service.create_issue(auth_user_id, auth_user_agent_id, subject, description)

        mock_post.assert_called_once_with(
            url,
            data={
                "auth_user_id": auth_user_id,
                "auth_user_agent_id": auth_user_agent_id,
                "subject": subject,
                "description": description,
            },
            files=None
        )


if __name__ == '__main__':
    unittest.main()
