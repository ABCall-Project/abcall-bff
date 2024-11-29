from http import HTTPStatus
import unittest
import imaplib
from email.message import EmailMessage
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

    @patch('requests.post')
    def test_create_issue_success(self, post_mock):
        fake = Faker()
        issueService = IssueService()
        
        auth_user_id = fake.uuid4()
        auth_user_agent_id = fake.uuid4()
        subject = "Test Subject"
        description = "Test Description"

        mock_response = {
            "id": fake.uuid4(),
            "auth_user_id": auth_user_id,
            "auth_user_agent_id": auth_user_agent_id,
            "subject": subject,
            "description": description,
            "created_at": "2024-11-28T10:00:00Z",
        }
        post_mock.return_value = MagicMock(status_code=HTTPStatus.CREATED, json=MagicMock(return_value=mock_response))

        response = issueService.create_issue(auth_user_id, auth_user_agent_id, subject, description)

        self.assertEqual(response, mock_response)

    @patch('requests.post')
    def test_create_issue_error_status_code(self, post_mock):
        fake = Faker()
        issueService = IssueService()
        
        auth_user_id = fake.uuid4()
        auth_user_agent_id = fake.uuid4()
        subject = "Test Subject"
        description = "Test Description"

        post_mock.return_value = MagicMock(status_code=HTTPStatus.BAD_REQUEST, text="Invalid data")

        response = issueService.create_issue(auth_user_id, auth_user_agent_id, subject, description)

        self.assertIsNone(response)

    @patch('requests.post')
    def test_create_issue_raises_exception(self, post_mock):
        fake = Faker()
        issueService = IssueService()
        
        auth_user_id = fake.uuid4()
        auth_user_agent_id = fake.uuid4()
        subject = "Test Subject"
        description = "Test Description"

        post_mock.side_effect = requests.exceptions.RequestException("Connection error")

        with self.assertRaises(requests.exceptions.RequestException):
            issueService.create_issue(auth_user_id, auth_user_agent_id, subject, description)


    @patch('imaplib.IMAP4_SSL')
    def test_process_incoming_emails_imap_error(self, imap_mock):
        fake_mail = MagicMock()
        imap_mock.return_value = fake_mail
        fake_mail.login.side_effect = imaplib.IMAP4.error("Login failed")

        issueService = IssueService()
        issueService.logger = MagicMock()

        issueService.process_incoming_emails()

        issueService.logger.error.assert_called_with("IMAP login failed. Check credentials or account status.")

        fake_mail.select.assert_not_called()
        fake_mail.search.assert_not_called()

    @patch('imaplib.IMAP4_SSL')
    def test_process_incoming_emails_fetch_error(self, imap_mock):
        fake_mail = MagicMock()
        imap_mock.return_value = fake_mail

        fake_mail.login.return_value = 'OK', []
        fake_mail.select.return_value = 'OK', []

        fake_mail.search.return_value = 'OK', [b'1']

        fake_mail.fetch.return_value = 'NO', []

        issueService = IssueService()
        issueService.logger = MagicMock()

        issueService.process_incoming_emails()

        issueService.logger.warning.assert_called_with("Failed to fetch email ID b'1'. Skipping.")

    def test_parse_email_to_issue(self):
        issueService = IssueService()

        subject = "Test Email Subject"
        body = "This is the body of the email."

        issue_data = issueService.parse_email_to_issue(subject, body)

        self.assertEqual(issue_data['subject'], subject)
        self.assertEqual(issue_data['description'], body)
        self.assertEqual(issue_data['auth_user_id'], "default_user")
        self.assertEqual(issue_data['auth_user_agent_id'], "default_agent")
        self.assertIsNone(issue_data['file_path'])

    @patch('requests.get')
    def test_get_top_seven_issues_success(self, get_mock):
        issueService = IssueService()
        
        mock_response = {
            "issues": [
                {"id": "1", "subject": "Issue 1"},
                {"id": "2", "subject": "Issue 2"},
            ]
        }
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK, json=MagicMock(return_value=mock_response))

        response = issueService.get_top_seven_issues()

        self.assertEqual(response, mock_response)


    @patch('requests.get')
    def test_get_top_seven_issues_error_status(self, get_mock):
        issueService = IssueService()
        
        get_mock.return_value = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        response = issueService.get_top_seven_issues()

        self.assertIsNone(response)


    @patch('requests.get')
    def test_get_top_seven_issues_raises_exception(self, get_mock):
        issueService = IssueService()
        
        get_mock.side_effect = requests.exceptions.RequestException("Connection error")

        with self.assertRaises(requests.exceptions.RequestException):
            issueService.get_top_seven_issues()

    @patch('requests.get')
    def test_get_predicted_data_success(self, get_mock):
        issueService = IssueService()
        
        mock_response = {
            "predictions": [
                {"id": "1", "score": 0.95},
                {"id": "2", "score": 0.89},
            ]
        }
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK, json=MagicMock(return_value=mock_response))

        response = issueService.get_predicted_data()

        self.assertEqual(response, mock_response)


    @patch('requests.get')
    def test_get_predicted_data_error_status(self, get_mock):
        issueService = IssueService()
        
        get_mock.return_value = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        response = issueService.get_predicted_data()

        self.assertIsNone(response)


    @patch('requests.get')
    def test_get_predicted_data_raises_exception(self, get_mock):
        issueService = IssueService()
        
        get_mock.side_effect = requests.exceptions.RequestException("Connection error")

        with self.assertRaises(requests.exceptions.RequestException):
            issueService.get_predicted_data()