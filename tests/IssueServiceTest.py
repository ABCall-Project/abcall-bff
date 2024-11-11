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

