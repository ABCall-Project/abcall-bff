import unittest
from unittest.mock import patch, MagicMock
from flaskr.service.IssueService import IssueService

class IssueServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = IssueService()

    @patch('flaskr.service.IssueService.requests.get')  # Mockeando requests.get
    def test_get_answer_ai_success(self, mock_get):
        # Simulamos una respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'answer': 'This is the AI answer'}
        mock_get.return_value = mock_response

        question = 'What is AI?'
        answer = self.service.get_answer_ai(question)

        self.assertIsNotNone(answer)
        self.assertEqual(answer, 'This is the AI answer')

    @patch('flaskr.service.IssueService.requests.get')
    def test_get_answer_ai_no_response(self, mock_get):
        # Simulamos una respuesta 200 pero sin datos
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        question = 'What is AI?'
        answer = self.service.get_answer_ai(question)

        self.assertIsNone(answer)

    @patch('flaskr.service.IssueService.requests.get')
    def test_get_answer_ai_not_found(self, mock_get):
        # Simulamos un código de estado 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        question = 'What is AI?'
        answer = self.service.get_answer_ai(question)

        self.assertIsNone(answer)

    @patch('flaskr.service.IssueService.requests.get')
    def test_get_answer_ai_exception(self, mock_get):
        # Simulamos una excepción al hacer la petición
        mock_get.side_effect = Exception("Connection Error")

        question = 'What is AI?'
        answer = self.service.get_answer_ai(question)

        self.assertIsNone(answer)
