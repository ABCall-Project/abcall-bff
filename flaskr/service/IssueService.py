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

class IssueService:
    """
    This class is for integrate the bff with the Issue service
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
        self.logger.info(f'Instanced issue service')
        self.base_url = os.environ.get('ISSUE_API_PATH')

    
        
    
    def get_answer_ai(self,question):
        """
        method to ask question to chat gpt
        Args:
            question (str): question to ask
        Return:
            answer (str): answer about ask
        """
        answer=''
        try:
            self.logger.info(f'init consuming api openai {self.base_url}')
            response = requests.get(f'{self.base_url}/issue/getIAResponse?question={question}')
            self.logger.info(f'quering open ai')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering open ai')
                data = response.json()
                if data:
                    self.logger.info(f'there are answer response ')
                    answer=data.get('answer')

                    return answer
                    
                else:
                    self.logger.info(f'there arent response')
                    return None
            else:
                self.logger.info(f"error consuming open ai: {response.status_code}")
                return None
        except Exception as e:
            self.logger.info(f"Error comunication with open ai: {str(e)}")
            return None
        
