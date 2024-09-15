import json
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

        # invoice_list=[]
        # for invoice_item in invoices:
        #     print(invoice_item.customer_id)
            
        #     invoice={
        #         "id": invoice_item.id,
        #         "customer_id": str(invoice_item.customer_id),
        #         "invoice_id": invoice_item.invoice_id,
        #         "payment_id": invoice_item.payment_id if invoice_item.payment_id else None,
        #         "amount": invoice_item.amount,
        #         "tax": invoice_item.tax,
        #         "total_amount": invoice_item.total_amount,
        #         "subscription": invoice_item.subscription,
        #         "subscription_id": str(invoice_item.subscription_id),
        #         "status": invoice_item.status,
        #         "created_at": invoice_item.created_at.isoformat() if invoice_item.created_at else None,
        #         "updated_at": invoice_item.updated_at.isoformat() if invoice_item.updated_at else None,
        #         "generation_date": invoice_item.generation_date.isoformat() if invoice_item.generation_date else None,
        #         "period": invoice_item.period if invoice_item.period else None

        #     }
        #     invoice_list.append(invoice)

            
            
        # return jsonify(invoice_list)
