from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...service.InvoiceService import *
from ...models.Invoice import *

class InvoiceView(Resource):
    """
    This class represent a invoce api view
    Attributes:
        na
    """

    def get(self,id_suscription):
        """
        this method is to query invoices from id suscription

        Args: 
                id_suscription (string): suscription id
        Returns:
            post (Post) 
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'receiving request of query invoices by suscription {id_suscription}')
        payment_service=PaymentService()
        invoices= payment_service.get_invoices_by_suscription(id_suscription)
        if invoices is None:
            return None, HTTPStatus.NOT_FOUND
        return invoices