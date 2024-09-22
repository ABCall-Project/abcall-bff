from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from config import Config


class ReportService:
    """
    This class is for integrate the bff with the Reports api
    Attributes:
        base_url (string): the payment api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        self.config=Config()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instancing Reports service')
        self.base_url = self.config.URL_REPORTS_SERVICE

    def download_invoice_by_id(self, invoice_id):
        """
        method to download invoice document in pdf format
        Args:
            invoice_id (str): id invoice
        Return
            pdfdocument (byte[]): document to download
        """
        try:
            self.logger.info(f'init consuming api reports {self.base_url}/invoice/{invoice_id}')
            response=requests.get(f'{self.base_url}/invoice/{invoice_id}')
            self.logger.info('downloading invoice')
            if response.status_code==200:
                self.logger.info('status code 200 downloading invoice')
                return response.content
            else:
                self.logger.info(f'error consuming report service api {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error comunication with reports api {str(e)}')
            return None