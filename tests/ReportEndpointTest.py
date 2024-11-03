import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from http import HTTPStatus
from io import BytesIO
from flaskr.endpoint.reports.Report import ReportView

class ReportViewTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(ReportView, '/invoice/<string:invoice_id>')
        self.client = self.app.test_client()

    @patch('flaskr.service.ReportService.download_invoice_by_id')
    def test_get_invoice_success(self, mock_download_invoice):
        # Configuramos el mock para que devuelva contenido de bytes
        mock_download_invoice.return_value = BytesIO(b'PDF content of invoice')

        invoice_id = 'INV-001'
        response = self.client.get(f'/invoice/{invoice_id}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content_type, 'application/octet-stream')
        self.assertIn(b'PDF content of invoice', response.data)
        self.assertEqual(response.headers['Content-Disposition'], f'attachment; filename=invoice-{invoice_id}.pdf')

    @patch('flaskr.service.ReportService.download_invoice_by_id')
    def test_get_invoice_not_found(self, mock_download_invoice):
        # Configuramos el mock para que devuelva None, simulando que no se encontró la factura
        mock_download_invoice.return_value = None

        invoice_id = 'INV-002'
        response = self.client.get(f'/invoice/{invoice_id}')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


    @patch('flaskr.service.ReportService.download_invoice_by_id')
    def test_get_invoice_internal_error(self, mock_download_invoice):
        # Simulamos una excepción en el servicio
        mock_download_invoice.side_effect = Exception('Service error')

        invoice_id = 'INV-003'
        response = self.client.get(f'/invoice/{invoice_id}')

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json['message'], 'Something was wrong trying download invoice')

