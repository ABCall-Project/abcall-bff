from http import HTTPStatus
import unittest
from unittest.mock import patch, MagicMock, Mock
from faker import Faker
from builder import FindIssueBuilder
from flaskr.service.IssueService import IssueService
from tests.builder import IssueBuilder
import requests



class IssueServiceTestCase(unittest.TestCase):
    @patch('requests.get')
    def test_return_none_when_status_code_is_not_ok(self, get_mock):
        fake = Faker()
        user_id = fake.uuid4()
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        issues = issueService.get_issue_by_user_id(user_id=user_id,page=1, limit=10)

        self.assertIsNone(issues)

    @patch('requests.get')
    def test_return_an_error_if_some_exception_error_occurred(self, get_mock):
        fake = Faker()
        user_id = fake.uuid4()
        issueService = IssueService()
        
        get_mock.side_effect = requests.exceptions.RequestException("Some weird error ocurred 🤯")
        
        with self.assertRaises(requests.exceptions.RequestException):
            issueService.get_issue_by_user_id(user_id=user_id, page=1, limit=10)


    @patch('requests.get')
    def test_return_a_list_of_issue_for_pagination(self, get_mock):
        fake = Faker()
        user_id = fake.uuid4()
        issues = []
        issue =  IssueBuilder().build()
        issues.append(issue)
        issue_mock = FindIssueBuilder().with_data(issues).build()
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = issue_mock
        expected_response = {
            'hasNext': issue_mock['has_next'],
            'totalPages': issue_mock['total_pages'],
            'page': issue_mock['page'],
            'limit': issue_mock['limit'],
            'data': []
        }

        for issue in issue_mock['data']:
            expected_response['data'].append({
                "id": issue['id'],
                "authUserId": issue['auth_user_id'],
                "description": issue['description'],
                "status": issue['status'],
                "subject": issue['subject'],
                "createdAt": issue['created_at'],
                "closedAt": issue['closed_at'],
                "channelPlanId": issue['channel_plan_id']
            })

        response = issueService.get_issue_by_user_id(user_id=user_id,page=1, limit=10)

        self.assertEqual(response, expected_response)

    @patch('requests.get')
    def test_return_a_list_of_issues(self, get_mock):
        issues = []
        issue =  IssueBuilder().build()
        issues.append(issue)
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = issues

        response = issueService.get_all_issues()

        self.assertEqual(response, issues)

    @patch('requests.post')
    def test_should_be_assign_an_issue(self, post_mock):
        fake = Faker()

        issue_id = IssueBuilder().with_id(fake.uuid4())
        issueService = IssueService()
        
        auth_user_agent_id = str(fake.uuid4())
        post_mock.return_value = MagicMock(status_code=HTTPStatus.OK, json=MagicMock(return_value=issue_id))
        response = issueService.assign_issue(issue_id, auth_user_agent_id)

        self.assertEqual(response, issue_id)

    @patch('requests.post')
    def test_should_handle_exception_when_communicating_with_service(self, post_mock):
        fake = Faker()

        issue_id = fake.uuid4()
        auth_user_agent_id = str(fake.uuid4())
        issueService = IssueService()
        
        post_mock.side_effect = requests.exceptions.RequestException("Error de conexión")
        
        with self.assertRaises(requests.exceptions.RequestException):
            issueService.assign_issue(issue_id, auth_user_agent_id)

    @patch('requests.get')
    def test_return_none_when_status_code_is_not_ok(self, get_mock):
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        issues = issueService.get_open_issues(page=1, limit=10)

        self.assertIsNone(issues)
    
    @patch('requests.get')
    def test_return_a_list_of_open_issue_for_pagination(self, get_mock):
        fake = Faker()
        user_id = fake.uuid4()
        issues = []
        issue =  IssueBuilder().build()
        issues.append(issue)
        issue_mock = FindIssueBuilder().with_data(issues).build()
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = issue_mock
        expected_response = {
            'hasNext': issue_mock['has_next'],
            'totalPages': issue_mock['total_pages'],
            'page': issue_mock['page'],
            'limit': issue_mock['limit'],
            'data': []
        }

        for issue in issue_mock['data']:
            expected_response['data'].append({
                "id": issue['id'],
                "authUserId": issue['auth_user_id'],
                "description": issue['description'],
                "status": issue['status'],
                "subject": issue['subject'],
                "createdAt": issue['created_at'],
                "closedAt": issue['closed_at'],
                "channelPlanId": issue['channel_plan_id']
            })

        response = issueService.get_open_issues(page=1, limit=10)
        self.assertEqual(response, expected_response)

