import json
from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...service.InvoiceService import *
from ...models.Invoice import *
import logging
from ...service.IssueService import *

class InvoiceView(Resource):
    """
    This class represent a invoce api view
    Attributes:
        na
    """

    def __init__(self):
        self.issue_service = IssueService()
        self.payment_service = PaymentService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')


    def get(self, action=None):
        if action == 'getInvoices':
            return self.getInvoices()
        elif action=='getTotalCostPending':
            return self.get_total_cost_pending()
        elif action=='getListDetailsInvoiceById':
            return self.get_list_details_invoice_by_id()
        elif action == 'getIAResponse':
            return self.getIAResponse()
        elif action == 'getIssuesDashboard':
            return self.getIssuesDashboard()
        else:
            return {"message": "Action not found"}, 404

    def getInvoices(self):
        """
        This method is to query invoices from customer id.

        Args: 
            customer_id (UUID): customer id
        Returns:
            JSON response containing the invoices or an error message.
        """
        customer_id = request.args.get('customer_id')
        
        
        self.logger.info(f'receiving request of query invoices by customer id: {customer_id}')
        

        invoices = self.payment_service.get_invoices_by_customer(customer_id)


        if not invoices: 
            return {"message": "No invoices found"}, HTTPStatus.NOT_FOUND

        invoices_list = [invoice.to_dict() for invoice in invoices]
        return invoices_list, HTTPStatus.OK
    
    def get_total_cost_pending(self):

        try:
            customer_id = request.args.get('customer_id')
            self.logger.info(f'Receive request to get total cost of customer_id {customer_id}')
            total_cost = self.payment_service.get_total_cost_pending(customer_id)
            return {
                'total_cost': float(total_cost)
            }, HTTPStatus.OK
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to get total cost of {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get total cost'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    
    def get_list_details_invoice_by_id(self):
        try:

            self.logger.info(f'Receive request to get invoice details')

            invoice_id = request.args.get('invoice_id')
            invoice_detail_list = self.payment_service.get_invoice_details(invoice_id)
            list_details = [detail.to_dict() for detail in invoice_detail_list]
            
            return list_details, HTTPStatus.OK
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to get invoice details: {ex}')
            return {'message': 'Something was wrong trying to get invoice details'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def getIAResponse(self):
        try:
            self.logger.info(f'Receive request to ask to open ai')
            question = request.args.get('question')
            answer=self.issue_service.get_answer_ai(question)
            return {
                'answer': answer
            }, HTTPStatus.OK
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying ask open ai: {ex}')
            return {'message': 'Something was wrong trying ask open ai'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def getIssuesDashboard(self):
        try:
            self.logger.info(f'Receive request to get issues dashboard')

            customer_id = request.args.get('customer_id')
            status = request.args.get('status')
            channel_plan_id = request.args.get('channel_plan_id')
            created_at = request.args.get('created_at')
            closed_at = request.args.get('closed_at')

            issues = self.issue_service.get_issues_dashboard(
                customer_id=customer_id,
                status=status,
                channel_plan_id=channel_plan_id,
                created_at=created_at,
                closed_at=closed_at
            )

            if not issues:
                return {"message": "No issues found"}, HTTPStatus.NOT_FOUND

            return issues, HTTPStatus.OK

        except Exception as ex:
            self.logger.error(f'Some error occurred trying to get issues dashboard: {ex}')
            return {'message': 'Something went wrong trying to get issues dashboard'}, HTTPStatus.INTERNAL_SERVER_ERROR