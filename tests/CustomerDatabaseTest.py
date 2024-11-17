import unittest
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from uuid import uuid4
from flaskr.app import app

class CustomerDatabaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    @patch('flaskr.service.CustomerDatabaseService.load_entries')
    def test_post_load_entries_success(self, load_entries_mock):
        fake_customer_id = str(uuid4())
        fake_entries = [
            {"topic": "Topic 1", "content": "Content 1"},
            {"topic": "Topic 2", "content": "Content 2"}
        ]
        mock_response = [
            {
                "id": str(uuid4()),
                "customer_id": fake_customer_id,
                "topic": "Topic 1",
                "content": "Content 1",
                "created_at": "2024-11-14T12:00:00"
            },
            {
                "id": str(uuid4()),
                "customer_id": fake_customer_id,
                "topic": "Topic 2",
                "content": "Content 2",
                "created_at": "2024-11-14T12:05:00"
            }
        ]
        load_entries_mock.return_value = mock_response

        response = self.client.post(
            '/customerDatabase/loadEntries',
            json={"customer_id": fake_customer_id, "entries": fake_entries}
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json, mock_response)

    @patch('flaskr.service.CustomerDatabaseService.load_entries')
    def test_post_load_entries_failure(self, load_entries_mock):
        fake_customer_id = str(uuid4())
        fake_entries = [{"topic": "Topic 1", "content": "Content 1"}]
        load_entries_mock.return_value = None

        response = self.client.post(
            '/customerDatabase/loadEntries',
            json={"customer_id": fake_customer_id, "entries": fake_entries}
        )

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json, {"message": "Failed to load entries"})

    @patch('flaskr.service.CustomerDatabaseService.load_entries')
    def test_post_load_entries_invalid_request(self, load_entries_mock):
        response = self.client.post(
            '/customerDatabase/loadEntries',
            json={"entries": []}  # Missing customer_id
        )

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("message", response.json)

    @patch('flaskr.service.CustomerDatabaseService.load_entries')
    def test_post_load_entries_exception(self, load_entries_mock):
        fake_customer_id = str(uuid4())
        fake_entries = [{"topic": "Topic 1", "content": "Content 1"}]
        load_entries_mock.side_effect = Exception("Unexpected error")

        response = self.client.post(
            '/customerDatabase/loadEntries',
            json={"customer_id": fake_customer_id, "entries": fake_entries}
        )

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json, {'message': 'An error occurred while loading entries'})
