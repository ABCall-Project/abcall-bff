import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from flask_testing import TestCase
from http import HTTPStatus
from flaskr.endpoint.invoice.Invoice import InvoiceView


class InvoiceViewTestCase(TestCase):
    
    def create_app(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(InvoiceView, '/invoices/<string:action>')
        return app

    @patch('flaskr.endpoint.invoice.Invoice.PaymentService')  # Mockeando el servicio de pagos
    def test_get_invoices_success(self, mock_payment_service):
        mock_service = mock_payment_service.return_value
        mock_service.get_invoices_by_customer.return_value = [MagicMock(to_dict=lambda: {"id": "123", "total": 100})]

        with self.client:
            response = self.client.get('/invoices/getInvoices', query_string={'customer_id': '12345'})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(response.json, [{"id": "123", "total": 100}])

    @patch('flaskr.endpoint.invoice.Invoice.PaymentService')
    def test_get_invoices_not_found(self, mock_payment_service):
        mock_service = mock_payment_service.return_value
        mock_service.get_invoices_by_customer.return_value = []

        with self.client:
            response = self.client.get('/invoices/getInvoices', query_string={'customer_id': '12345'})
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            self.assertEqual(response.json, {"message": "No invoices found"})

    @patch('flaskr.endpoint.invoice.Invoice.PaymentService')
    def test_get_total_cost_pending_success(self, mock_payment_service):
        mock_service = mock_payment_service.return_value
        mock_service.get_total_cost_pending.return_value = 150.75

        with self.client:
            response = self.client.get('/invoices/getTotalCostPending', query_string={'customer_id': '12345'})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(response.json, {'total_cost': 150.75})

    @patch('flaskr.endpoint.invoice.Invoice.PaymentService')
    def test_get_list_details_invoice_by_id_success(self, mock_payment_service):
        mock_service = mock_payment_service.return_value
        mock_service.get_invoice_details.return_value = [MagicMock(to_dict=lambda: {"detail": "Some detail", "amount": 50})]

        with self.client:
            response = self.client.get('/invoices/getListDetailsInvoiceById', query_string={'invoice_id': 'INV12345'})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(response.json, [{"detail": "Some detail", "amount": 50}])

    @patch('flaskr.endpoint.invoice.Invoice.PaymentService')
    def test_get_list_details_invoice_by_id_error(self, mock_payment_service):
        mock_service = mock_payment_service.return_value
        mock_service.get_invoice_details.side_effect = Exception("Some error")

        with self.client:
            response = self.client.get('/invoices/getListDetailsInvoiceById', query_string={'invoice_id': 'INV12345'})
            self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
            self.assertEqual(response.json, {'message': 'Something was wrong trying to get invoice details'})

