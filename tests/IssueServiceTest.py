from http import HTTPStatus
import unittest
from unittest.mock import patch, MagicMock, Mock
from faker import Faker
from builder import FindIssueBuilder
from flaskr.service.IssueService import IssueService
from tests.builder import IssueBuilder


class IssueServiceTestCase(unittest.TestCase):
    @patch('requests.get')
    def test_return_none_when_status_code_is_not_ok(self, get_mock):
        fake = Faker()
        user_id = fake.uuid4()
        issueService = IssueService()
        get_mock.return_value = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        issues = issueService.get_issue_by_user_id(user_id=user_id,page=1, limit=10)

        self.assertIsNone(issues)

    def test_return_an_error_if_some_exception_error_occurred(self):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = SystemError("Some weird error ocurred 🤯")

        with patch('requests.get', return_value=mock_response):
            fake = Faker()
            user_id = fake.uuid4()
            issueService = IssueService()

            with self.assertRaises(SystemError):
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

        response = issueService.get_issue_by_user_id(user_id=user_id,page=1, limit=10)

        self.assertEqual(response, issue_mock)

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
    def test_should_be_assign_an_issue(self, get_mock):
            return_message = "Some error ocurred trying to assign_issue issues"
            fake = Faker()

            issue_id =  IssueBuilder().with_id(fake.uuid4())
            issueService = IssueService()
            
            auth_user_agent_id = str(fake.uuid4())
            get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
            response = issueService.assign_issue(issue_id,auth_user_agent_id)
            self.assertEqual(response, return_message)

    @patch('requests.post')
    def test_should_return_internal_server_error_if_some_error_occurred(self, get_mock):
            error_message = "Some error ocurred trying to assign_issue issues"
            get_mock.side_effect = SystemError('Some weird error ocurred 🤯')
            fake = Faker()
            issue_id = str(fake.uuid4())
            auth_user_agent_id = str(fake.uuid4())
            data = {
                "auth_user_agent_id": auth_user_agent_id
            }

            response = self.client.post(
                f'/issues/assignIssue?user_id={issue_id}',
                json=data  
            )

            self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
            self.assertEqual(response.json["message"], error_message)

