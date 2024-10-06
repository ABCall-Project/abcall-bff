import json
from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...service.InvoiceService import *
from ...models.Invoice import *
import logging

class InvoiceView(Resource):
    """
    This class represent a invoce api view
    Attributes:
        na
    """

    def get(self, customer_id):
        """
        This method is to query invoices from customer id.

        Args: 
            customer_id (UUID): customer id
        Returns:
            JSON response containing the invoices or an error message.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'receiving request of query invoices by customer id: {customer_id}')
        
        payment_service = PaymentService()
        invoices = payment_service.get_invoices_by_customer(customer_id)


        if not invoices: 
            return {"message": "No invoices found"}, HTTPStatus.NOT_FOUND

        invoices_list = [invoice.to_dict() for invoice in invoices]
        return invoices_list, HTTPStatus.OK
