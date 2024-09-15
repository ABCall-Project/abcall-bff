from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.Invoice import Invoice

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
            
            self.logger.info(f'init consuming api invoices {self.base_url}/invoices/{customer_id}')
            response = requests.get(f'{self.base_url}/invoices/{customer_id}')
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
                                item.get('paymentId'),
                                item.get('amount'),
                                item.get('tax'),
                                item.get('totalAmount'),
                                item.get('subscription'),
                                item.get('subscriptionId'),
                                item.get('status'),
                                item.get('createdAt'),
                                item.get('updatedAt'),
                                item.get('generationDate'),                            
                                item.get('period')                          
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