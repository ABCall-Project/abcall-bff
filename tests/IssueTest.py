import unittest
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from faker import Faker
from flaskr.app import app
from builder import FindIssueBuilder, InvoiceResponseBuilder, InvoiceDataResponseBuilder
from flaskr.service.adapters.issue_mappers import issues_pagination_mapper

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

    @patch('requests.get')
    def test_should_get_a_pagination_list_of_issues(self, get_mock):
        fake = Faker()
        issues = []
        user_id = str(fake.uuid4())
        issues.append(InvoiceDataResponseBuilder() \
                        .with_auth_user_id(user_id)
                     .build())
        issues_mock = FindIssueBuilder() \
                      .with_data(issues) \
                    .build()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = issues_mock

        response = self.client.get(f'/issues/find?user_id={user_id}&page=1&limit=5')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, issues_pagination_mapper(issues_mock))


    @patch('requests.get')
    def test_should_return_not_found_when_there_is_not_any_data(self, get_mock):
        fake = Faker()
        user_id = str(fake.uuid4())
        issues_mock = {}
        get_mock.return_value = MagicMock(status_code=HTTPStatus.NOT_FOUND)
        get_mock.return_value.json.return_value = issues_mock

        response = self.client.get(f'/issues/find?user_id={user_id}&page=1&limit=5')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json, {})

    @patch('requests.get')
    def test_should_return_internal_server_error_if_some_error_occurred(self, get_mock):
        error_message = "Some error ocurred trying to get issues by user id"
        fake = Faker()
        user_id = str(fake.uuid4())
        get_mock.side_effect = SystemError('Some weird error ocurred 🤯')

        response = self.client.get(f'/issues/find?user_id={user_id}&page=1&limit=5')

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json["message"], error_message)