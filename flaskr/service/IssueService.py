from datetime import date
from email import message_from_bytes
import imaplib
from typing import Optional
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..models.Invoice import Invoice
from ..models.invoice_detail import InvoiceDetail
from .adapters.issue_mappers import issues_pagination_mapper

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
        """
        try:
            url = f'{self.base_url}/issue/getIssuesDasboard'
            params = {
                'customer_id': customer_id,
                'status': status,
                'channel_plan_id': channel_plan_id,
                'created_at': created_at,
                'closed_at': closed_at
            }
            params = {key: value for key, value in params.items() if value is not None}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f'Error querying issue dashboard service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue dashboard service: {str(e)}')
            return None
        
    def get_issue_by_user_id(self, user_id:str, page:int, limit:int):
        try:
            url = f'{self.base_url}/issues/find/{user_id}'
            params = {
                'page': page,
                'limit': limit
            }
            params = {key: value for key, value in params.items() if value is not None}
            response = requests.get(url, params=params)

            if response.status_code == HTTPStatus.OK:
                return issues_pagination_mapper(response.json())
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e


    def get_ia_predictive_answer(self,user_id):
        """
        method to ask predictive analitic
        Args:
            user_id (str): id user to build de context
        Return:
            answer (str): answer about ask
        """
        answer=''
        try:
            self.logger.info(f'init consuming api predictive ia {self.base_url}/issue/getIAPredictiveAnswer?user_id={user_id}')
            response = requests.get(f'{self.base_url}/issue/getIAPredictiveAnswer?user_id={user_id}')
            self.logger.info(f'quering predictive ia')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering predictive ia')
                data = response.json()
                if data:
                    self.logger.info(f'there are answer response ')
                    answer=data.get('answer')

                    return answer
                    
                else:
                    self.logger.info(f'there arent response')
                    return None
            else:
                self.logger.info(f"error consuming predictive ia: {response.status_code}")
                return None
        except Exception as e:
            self.logger.info(f"Error comunication with predictive ia: {str(e)}")
            return None

    def get_issue_detail(self, customer_id: str, issue_id: str) -> Optional[dict]:
        try:
            url = f'{self.base_url}/issue/get_issue_by_id'
            params = {
                'customer_id': customer_id,
                'issue_id': issue_id
            }
            response = requests.get(url, params=params)

            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e

    def get_all_issues(self) -> Optional[dict]:
        try:
            url = f'{self.base_url}/issue/getAllIssues'
          
            response = requests.get(url)

            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e

    def assign_issue(self, issue_id:str, auth_user_agent_id:str) -> Optional[dict]:
        try:
            url = f'{self.base_url}/issue/assignIssue?issue_id={issue_id}'
            data = {"auth_user_agent_id": auth_user_agent_id}
          
            response = requests.post(url, json=data)

            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error assign_issue issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e
    
    def get_open_issues(self, page:int, limit:int):
        try:
            url = f'{self.base_url}/issue/getOpenIssues'
            params = {
                'page': page,
                'limit': limit
            }
            params = {key: value for key, value in params.items() if value is not None}
            response = requests.get(url, params=params)

            if response.status_code == HTTPStatus.OK:
                return issues_pagination_mapper(response.json())
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e
        

    def get_top_seven_issues(self) -> Optional[dict]:
        try:
            url = f'{self.base_url}/issue/getTopSevenIssues'
          
            response = requests.get(url)

            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e
        
    
    def get_predicted_data(self) -> Optional[dict]:
        try:
            url = f'{self.base_url}/issue/getPredictedData'
          
            response = requests.get(url)

            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                self.logger.error(f'Error querying issue service: {response.status_code}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issue service: {str(e)}')
            raise e
        
    def create_issue(self, auth_user_id: str, auth_user_agent_id: str, subject: str, description: str, file_path: Optional[str] = None) -> Optional[dict]:        
        try:
            url = f'{self.base_url}/issue/createIssue'
            data = {
                "auth_user_id": auth_user_id,
                "auth_user_agent_id": auth_user_agent_id,
                "subject": subject,
                "description": description,
            }
            files = None
            if file_path:
                files = {"file": open(file_path, "rb")}
            
            response = requests.post(url, data=data, files=files)

            if response.status_code == HTTPStatus.CREATED:
                return response.json()
            else:
                self.logger.error(f'Error creating issue: {response.status_code}, {response.text}')
                return None
        except Exception as e:
            self.logger.error(f'Error communicating with issues API: {str(e)}')
            raise e
        
    def process_incoming_emails(self):
        """
        Connect to Gmail, fetch emails, and create issues from them.
        """
        try:
            # Configuración del servidor de correo
            imap_server = os.environ.get('EMAIL_IMAP_SERVER', 'imap.gmail.com')
            email_user = os.environ.get('EMAIL_USER')
            self.logger.info(email_user)
            email_pass = os.environ.get('EMAIL_PASS')
            self.logger.info(email_pass)

            # Validar configuraciones
            if not (imap_server and email_user and email_pass):
                self.logger.error("Missing email configuration in environment variables.")
                return

            # Conexión al servidor IMAP
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_user, email_pass)
            mail.select('inbox')

            # Buscar correos no leídos
            status, messages = mail.search(None, 'UNSEEN')
            if status != "OK":
                self.logger.error("Failed to search emails")
                return

            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = message_from_bytes(response_part[1])
                        subject = msg['subject']
                        sender = msg['from']
                        body = msg.get_payload(decode=True).decode('utf-8')

                        issue_data = self.parse_email_to_issue(subject, body)

                        self.create_issue(
                            auth_user_id=issue_data['auth_user_id'],
                            auth_user_agent_id=issue_data['auth_user_agent_id'],
                            subject=issue_data['subject'],
                            description=issue_data['description'],
                            file_path=issue_data.get('file_path')
                        )

            mail.logout()
            self.logger.info("Email processing completed.")

        except Exception as e:
            self.logger.error(f"Error processing emails: {str(e)}")
            raise e

    def parse_email_to_issue(self, subject, body):
        """
        Parse the email subject and body into issue data.
        """
        return {
            "auth_user_id": "default_user",
            "auth_user_agent_id": "default_agent",
            "subject": subject,
            "description": body,
            "file_path": None 
        }