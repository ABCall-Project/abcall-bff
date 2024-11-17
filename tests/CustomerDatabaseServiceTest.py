import unittest
from unittest.mock import patch, MagicMock
import os
from flaskr.service.CustomerDatabaseService import CustomerDatabaseService
from uuid import uuid4

class CustomerDatabaseServiceTest(unittest.TestCase):

    def setUp(self):
        os.environ['CUSTOMER_API_PATH'] = 'http://fakeurl.com'
        self.service = CustomerDatabaseService()

    @patch('requests.post')  # Ajustar la ruta al uso correcto
    def test_load_entries_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = [
            {"id": str(uuid4()), "customer_id": str(uuid4()), "topic": "Topic 1", "content": "Content 1"},
            {"id": str(uuid4()), "customer_id": str(uuid4()), "topic": "Topic 2", "content": "Content 2"}
        ]
        mock_post.return_value = mock_response

        customer_id = uuid4()
        entries = [{"topic": "Topic 1", "content": "Content 1"}]
        result = self.service.load_entries(customer_id, entries)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)

    @patch('requests.post')
    def test_load_entries_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Internal Server Error"}
        mock_post.return_value = mock_response

        customer_id = uuid4()
        entries = [{"topic": "Topic 1", "content": "Content 1"}]
        result = self.service.load_entries(customer_id, entries)

        self.assertIsNone(result)

    @patch('requests.post')
    def test_load_entries_exception(self, mock_post):
        mock_post.side_effect = Exception("Some error occurred")

        customer_id = uuid4()
        entries = [{"topic": "Topic 1", "content": "Content 1"}]
        result = self.service.load_entries(customer_id, entries)

        self.assertIsNone(result)
