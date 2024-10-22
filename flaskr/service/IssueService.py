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
        
    def get_issues_dashboard(self, customer_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        """
        Method to retrieve issues from the dashboard using optional filters.
        Args:
            customer_id (str): ID of the customer.
            status (str): Status of the issues (optional).
            channel_plan_id (str): Channel plan ID (optional).
            created_at (str): Issues created after this date (optional).
            closed_at (str): Issues closed before this date (optional).
        Return:
            issues (list): List of issues filtered by the given criteria.
        """
        try:
            self.logger.info(f'Initiating request to {self.base_url}/issues/getIssuesDasboard')

            params = {
                'customer_id': customer_id,
                'status': status,
                'channel_plan_id': channel_plan_id,
                'created_at': created_at,
                'closed_at': closed_at
            }
            
            params = {key: value for key, value in params.items() if value is not None}

            response = requests.get(f'{self.base_url}/issues/getIssuesDasboard', params=params)
            
            if response.status_code == 200:
                self.logger.info(f'Successful query to issue dashboard service with status code 200')
                data = response.json()

                if data:
                    self.logger.info(f'Found issues in the response')
                    return data
                else:
                    self.logger.info(f'No issues found for the provided filters')
                    return []
            else:
                self.logger.error(f'Error querying issue dashboard service: {response.status_code}')
                return []
        except Exception as e:
            self.logger.error(f'Error communicating with issue dashboard service: {str(e)}')
            return []