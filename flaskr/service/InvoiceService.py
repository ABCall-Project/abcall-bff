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

    def get_invoices_by_suscription(self,id_suscription):
        """
        method to query invoices by suscription to payment services
        Args:
            id_suscription (string): id suscription
        Return:
            invoices (Invoice): list of invoice object
        """
        invoices=[]
        try:
            
            self.logger.info(f'init consuming api invoices {self.base_url}/invoices?suscription={id_suscription}')
            response = requests.get(f'{self.base_url}/invoices?suscription={id_suscription}')
            self.logger.info(f'quering invoices by suscription')
            if response.status_code == 200:
                self.logger.info(f'status code 200 queryng invoices on payment services')
                data = response.json()
                if data:
                    self.logger.info(f'there are invoices on payment services {data}')
                    invoices.append(Invoice(data.get('id'),
                            data.get('number_id'),
                            data.get('generated_date'),
                            data.get('period'),
                            data.get('mount'),
                            data.get('state'),
                            data.get('url_document'),
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