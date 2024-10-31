from unittest.mock import patch
import unittest
from http import HTTPStatus
from flaskr.app import app

class HealthCheckTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True
    
    def test_get_healthcheck(self):
        response = self.client.get('/health')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["environment"], "test")
        self.assertEqual(response.json["application"], "abcall-bff")
        self.assertEqual(response.json["status"], HTTPStatus.OK)
