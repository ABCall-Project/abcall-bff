import unittest
from unittest.mock import patch, MagicMock
import os
from flaskr.service.InvoiceService import PaymentService
from flaskr.service.InvoiceService import Invoice
from flaskr.service.InvoiceService import InvoiceDetail


class PaymentServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['PAYMENT_API_PATH'] = 'http://fakeurl.com'  
        self.service = PaymentService()

    @patch('flaskr.service.InvoiceService.requests.get')  
    def test_get_invoices_by_customer_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': '1',
                'customerId': '123',
                'invoiceId': 'INV-001',
                'planId': 'PLAN-001',
                'amount': 100.0,
                'tax': 15.0,
                'totalAmount': 115.0,
                'status': 'Paid',
                'createdAt': '2024-01-01T00:00:00',
                'startAt': '2024-01-01T00:00:00',
                'generationDate': '2024-01-01T00:00:00',
                'endAt': '2024-01-31T00:00:00',
                'plan_amount': 100.0,
                'issues_amount': 0.0
            }
        ]
        mock_get.return_value = mock_response

        customer_id = '123'
        invoices = self.service.get_invoices_by_customer(customer_id)
        
        self.assertIsNotNone(invoices)
        self.assertEqual(len(invoices), 1)
        self.assertIsInstance(invoices[0], Invoice)
        self.assertEqual(invoices[0].customer_id, '123')

    @patch('flaskr.service.InvoiceService.requests.get')
    def test_get_invoices_by_customer_not_found(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        customer_id = '123'
        invoices = self.service.get_invoices_by_customer(customer_id)
        
        self.assertIsNone(invoices)

    @patch('flaskr.service.InvoiceService.requests.get')
    def test_get_total_cost_pending_success(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'total_cost': 150.75}
        mock_get.return_value = mock_response

        customer_id = '123'
        total_cost = self.service.get_total_cost_pending(customer_id)
        
        self.assertEqual(total_cost, 150.75)

    @patch('flaskr.service.InvoiceService.requests.get')
    def test_get_invoice_details_success(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': '1',
                'detail': 'Detail 1',
                'invoice_id': 'INV-001',
                'issue_id': 'ISS-001',
                'amount': 50.0,
                'tax': 5.0,
                'total_amount': 55.0,
                'chanel_plan_id': 'PLAN-001',
                'issue_date': '2024-01-01'
            }
        ]
        mock_get.return_value = mock_response

        invoice_id = 'INV-001'
        details = self.service.get_invoice_details(invoice_id)

        self.assertIsNotNone(details)
        self.assertEqual(len(details), 1)
        self.assertIsInstance(details[0], InvoiceDetail)
        self.assertEqual(details[0].invoice_id, 'INV-001')

    @patch('flaskr.service.InvoiceService.requests.get')
    def test_get_invoice_details_not_found(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        invoice_id = 'INV-001'
        details = self.service.get_invoice_details(invoice_id)

        self.assertIsNone(details)

