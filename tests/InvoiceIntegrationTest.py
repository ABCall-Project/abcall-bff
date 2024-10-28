from unittest.mock import patch, MagicMock
import unittest
from http import HTTPStatus
from flaskr.app import app
from builder import InvoiceResponseBuilder,InvoiceDetailResponseBuilder

class InvoiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True
    
    def test_should_return_not_found_when_the_get_path_does_not_exist(self):
        error_message = "Action not found"

        response = self.client.get('/invoices/getFakePath')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json["message"], error_message)


    @patch("flaskr.service.InvoiceService.requests")
    def test_should_return_not_found_when_the_invoice_does_not_exist(self, requestsMock):
        error_message = "No invoices found"
        requestsMock.get.return_value = SystemError("Some weird error 🤯")

        response = self.client.get('/invoices/getInvoices?customer_id=customer-fake-id')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json["message"], error_message)

    @patch("flaskr.service.InvoiceService.requests.get")
    def test_should_return_a_invoice_list(self, get_mock):
        invoice_mock = InvoiceResponseBuilder().build()
        invoices_mocked = []
        invoices_mocked.append(invoice_mock)
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = invoices_mocked

        response = self.client.get(f'/invoices/getInvoices?customer_id={invoice_mock["customerId"]}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    @patch("flaskr.service.InvoiceService.requests")
    def test_should_return_internal_server_error_when_get_total_cost_pending(self, requestsMock):
        error_message = "Something was wrong trying to get total cost"
        requestsMock.get.return_value = SystemError("Some weird error 🤯")

        response = self.client.get('/invoices/getTotalCostPending')

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json["message"], error_message)
    
    @patch("flaskr.service.InvoiceService.requests")
    def test_should_return_when_get_list_details_invoice_by_id(self, requestsMock):
        error_message = "Something was wrong trying to get invoice details"
        requestsMock.get.return_value = SystemError("Some weird error 🤯")

        response = self.client.get('/invoices/getListDetailsInvoiceById')

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json["message"], error_message)

    @patch("flaskr.service.InvoiceService.requests.get")
    def test_should_return_a_invoice_list(self, get_mock):
        invoice_mock = InvoiceDetailResponseBuilder().build()
        invoices_mocked = []
        invoices_mocked.append(invoice_mock)
        get_mock.return_value = MagicMock(status_code=HTTPStatus.OK)
        get_mock.return_value.json.return_value = invoices_mocked

        response = self.client.get(f'/invoices/getListDetailsInvoiceById?invoice_id={invoice_mock["invoiceId"]}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
