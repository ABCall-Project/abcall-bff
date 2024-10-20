from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.Invoice import Invoice
from ..models.invoice_detail import InvoiceDetail

class PaymentService:
    """
    This class is for integrate the bff with the Payment api
    Attributes:
        base_url (string): the payment api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'Instanced Payment service')
        self.base_url = os.environ.get('PAYMENT_API_PATH')

    def get_invoices_by_customer(self,customer_id):
        """
        method to query invoices by customer id to payment services
        Args:
            customer_id (UUID): id customer
        Return:
            invoices (Invoice): list of invoice object
        """
        invoices=[]
        try:
            
            self.logger.info(f'init consuming api invoices {self.base_url}/invoices/getInvoices?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/invoices/getInvoices?customer_id={customer_id}')
            self.logger.info(f'quering invoices by customer')
            if response.status_code == 200:
                self.logger.info(f'status code 200 queryng invoices on payment services')
                data = response.json()
                if data:
                    self.logger.info(f'there are invoices on payment services ')
                    for item in data:
                        invoices.append(Invoice(item.get('id'),
                                item.get('customerId'),
                                item.get('invoiceId'),
                                item.get('planId'),
                                item.get('amount'),
                                item.get('tax'),
                                item.get('totalAmount'),
                                item.get('status'),
                                item.get('createdAt'),
                                item.get('startAt'),
                                item.get('generationDate'),                            
                                item.get('endAt'),
                                item.get('plan_amount'),
                                item.get('issues_amount'),                          
                        ))
 
                    self.logger.info(f'deserializing invoice list')
                    return invoices
                    
                else:
                    self.logger.info(f'there arent invoices')
                    return None
            else:
                self.logger.info(f"error consuming invoice payment api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with invoice payment api: {str(e)}")
            return None
        
    
    def get_total_cost_pending(self,customer_id):
        """
        method to query total cost pending
        Args:
            customer_id (UUID): customer id
        Return:
            cost (float): cost pending value
        """
        cost=0
        try:
            
            self.logger.info(f'init consuming api customers {self.base_url}/invoices/getTotalCostPending?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/invoices/getTotalCostPending?customer_id={customer_id}')
            self.logger.info(f'quering cost pending ')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering cost pending  service')
                data = response.json()
                if data:
                    self.logger.info(f'there are cost pending response ')
                    cost=data.get('total_cost')

                    return cost
                    
                else:
                    self.logger.info(f'there arent response')
                    return None
            else:
                self.logger.info(f"error consuming cost pending api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with cost pending api: {str(e)}")
            return None
        


    def get_invoice_details(self,invoice_id):
        """
        method to query invoice details to payment services
        Args:
            invoice_id (UUID): id invoice
        Return:
            details (InvoiceDetail): list of invoice details
        """
        invoices_details=[]
        try:
            
            self.logger.info(f'init consuming api invoice details {self.base_url}/invoices/getListDetailsInvoiceById?invoice_id={invoice_id}')
            response = requests.get(f'{self.base_url}/invoices/getListDetailsInvoiceById?invoice_id={invoice_id}')
            self.logger.info(f'quering invoice details by invoice id')
            if response.status_code == 200:
                self.logger.info(f'status code 200 queryng invoice details on payment services')
                data = response.json()
                if data:
                    self.logger.info(f'there are invoice details on payment services ')
                    for item in data:

                        invoices_details.append(InvoiceDetail(item.get('id'),
                                item.get('detail'),
                                item.get('invoice_id'),
                                item.get('issue_id'),
                                item.get('amount'),
                                item.get('tax'),
                                item.get('total_amount'),
                                item.get('chanel_plan_id'),
                                item.get('issue_date')               
                        ))

 
                    self.logger.info(f'deserializing invoice detail list')
                    return invoices_details
                    
                else:
                    self.logger.info(f'there arent invoice details')
                    return None
            else:
                self.logger.info(f"error consuming invoice details payment api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with invoice details payment api: {str(e)}")
            return None