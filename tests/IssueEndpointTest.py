import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from http import HTTPStatus
from flaskr.endpoint.issue.Issue import IssueView

class IssueViewTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(IssueView, '/issues/<string:action>')
        self.client = self.app.test_client()

    @patch('flaskr.service.IssueService.IssueService.get_answer_ai')
    def test_getIAResponse_success(self, mock_get_answer_ai):
        mock_get_answer_ai.return_value = 'Sample AI answer'
        response = self.client.get('/issues/getIAResponse', query_string={'question': 'What is AI?'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'answer': 'Sample AI answer'})

    @patch('flaskr.service.IssueService.IssueService.get_answer_ai')
    def test_getIAResponse_error(self, mock_get_answer_ai):
        mock_get_answer_ai.side_effect = Exception('AI service error')
        response = self.client.get('/issues/getIAResponse', query_string={'question': 'What is AI?'})

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['message'], 'Something was wrong trying ask open ai')

    @patch('flaskr.service.IssueService.IssueService.get_issues_dashboard')
    def test_getIssuesDasboard_success(self, mock_get_issues_dashboard):
        mock_get_issues_dashboard.return_value = [{'issue_id': 1, 'status': 'open'}, {'issue_id': 2, 'status': 'closed'}]
        response = self.client.get('/issues/getIssuesDasboard', query_string={'customer_id': '123', 'status': 'open'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, [{'issue_id': 1, 'status': 'open'}, {'issue_id': 2, 'status': 'closed'}])

    @patch('flaskr.service.IssueService.IssueService.get_issues_dashboard')
    def test_getIssuesDasboard_not_found(self, mock_get_issues_dashboard):
        mock_get_issues_dashboard.return_value = []
        response = self.client.get('/issues/getIssuesDasboard', query_string={'customer_id': '123', 'status': 'open'})

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json['message'], 'No issues found')

    @patch('flaskr.service.IssueService.IssueService.get_issues_dashboard')
    def test_getIssuesDasboard_error(self, mock_get_issues_dashboard):
        mock_get_issues_dashboard.side_effect = Exception('Dashboard error')
        response = self.client.get('/issues/getIssuesDasboard', query_string={'customer_id': '123', 'status': 'open'})

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['message'], 'Something went wrong trying to get issues dashboard')

    @patch('flaskr.service.IssueService.IssueService.get_ia_predictive_answer')
    def test_get_ia_predictive_answer_success(self, mock_get_ia_predictive_answer):
        mock_get_ia_predictive_answer.return_value = 'Predictive AI response'
        response = self.client.get('/issues/getIAPredictiveAnswer', query_string={'user_id': '42'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'answer': 'Predictive AI response'})

    @patch('flaskr.service.IssueService.IssueService.get_ia_predictive_answer')
    def test_get_ia_predictive_answer_error(self, mock_get_ia_predictive_answer):
        mock_get_ia_predictive_answer.side_effect = Exception('Predictive AI error')
        response = self.client.get('/issues/getIAPredictiveAnswer', query_string={'user_id': '42'})

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['message'], 'Something was wrong trying ask predictive ai')

    def test_action_not_found(self):
        response = self.client.get('/issues/invalidAction')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json['message'], 'Action not found')
