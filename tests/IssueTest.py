import unittest
from http import HTTPStatus
from flaskr.app import app

class IssueTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True
    
    def test_should_return_not_found_when_the_get_path_does_not_exist(self):
        error_message = "Action not found"

        response = self.client.get('/issues/getFakePath')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json["message"], error_message)