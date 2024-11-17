import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from flaskr.service.CustomerDatabaseService import CustomerDatabaseService
import os

class CustomerDatabaseServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['CUSTOMER_API_PATH'] = 'http://abcall-url-fake.com'
        self.service = CustomerDatabaseService()

    @patch('requests.post')  # Ruta corregida
    def test_load_entries_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = [
            {
                "id": str(uuid4()),
                "customer_id": str(uuid4()),
                "topic": "Topic 1",
                "content": "Content 1",
                "created_at": "2024-11-14T12:00:00"
            },
            {
                "id": str(uuid4()),
                "customer_id": str(uuid4()),
                "topic": "Topic 2",
                "content": "Content 2",
                "created_at": "2024-11-14T12:05:00"
            }
        ]
        mock_post.return_value = mock_response

        customer_id = uuid4()
        entries = [
            {"topic": "Topic 1", "content": "Content 1"},
            {"topic": "Topic 2", "content": "Content 2"}
        ]

        result = self.service.load_entries(customer_id, entries)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["topic"], "Topic 1")
        self.assertEqual(result[1]["content"], "Content 2")

    @patch('requests.post')  # Ruta corregida
    def test_load_entries_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad Request"}
        mock_post.return_value = mock_response

        customer_id = uuid4()
        entries = []

        result = self.service.load_entries(customer_id, entries)

        self.assertIsNone(result)

    @patch('requests.post')  # Ruta corregida
    def test_load_entries_server_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        customer_id = uuid4()
        entries = [{"topic": "Topic 1", "content": "Content 1"}]

        result = self.service.load_entries(customer_id, entries)

        self.assertIsNone(result)

    @patch('requests.post')  # Ruta corregida
    def test_load_entries_exception(self, mock_post):
        mock_post.side_effect = Exception("Connection error")

        customer_id = uuid4()
        entries = [{"topic": "Topic 1", "content": "Content 1"}]

        result = self.service.load_entries(customer_id, entries)

        self.assertIsNone(result)
