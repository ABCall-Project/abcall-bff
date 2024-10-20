import unittest
from unittest.mock import patch, MagicMock
from flaskr.service.ReportService import ReportService
from config import Config 

class ReportServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = ReportService()

    @patch('flaskr.service.ReportService.requests.get') 
    def test_download_invoice_by_id_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'PDF document content' 
        mock_get.return_value = mock_response

        invoice_id = 'INV-001'
        pdf_document = self.service.download_invoice_by_id(invoice_id)
        
        self.assertIsNotNone(pdf_document)
        self.assertEqual(pdf_document, b'PDF document content')

    @patch('flaskr.service.ReportService.requests.get')
    def test_download_invoice_by_id_not_found(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        invoice_id = 'INV-001'
        pdf_document = self.service.download_invoice_by_id(invoice_id)

        self.assertIsNone(pdf_document)

    @patch('flaskr.service.ReportService.requests.get')
    def test_download_invoice_by_id_error(self, mock_get):
  
        mock_get.side_effect = Exception("Connection Error")

        invoice_id = 'INV-001'
        pdf_document = self.service.download_invoice_by_id(invoice_id)

        self.assertIsNone(pdf_document)

