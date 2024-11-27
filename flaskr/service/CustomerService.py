from datetime import date
from uuid import UUID
from flask import request
from http import HTTPStatus
import requests
import os
import logging

class CustomerService:
    """
    This class is for integrating the BFF with the Customer API.
    Attributes:
        base_url (string): The Customer API URL.
    """

    def __init__(self):
        """
        Service constructor.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instantiating Customer service')
        self.base_url = os.environ.get('CUSTOMER_API_PATH')
        self.logger.info(f'Customer API base URL: {self.base_url}')

    def add_customers(self, customers: list, plan_id: UUID) -> list:
        """
        Adds customers to the Customer API.

        Args:
            customers (list): List of dictionaries with 'document' and 'name' for each customer.
            plan_id (UUID): The subscription plan ID to associate with the customers.

        Returns:
            list: List of added customers as JSON or None if an error occurs.
        """
        try:
            self.logger.info(f'Sending request to add customers at {self.base_url}/customer/loadCustomers')
            payload = {
                "plan_id": str(plan_id),
                "customers": customers
            }
            response = requests.post(f'{self.base_url}/customer/loadCustomers', json=payload)

            if response.status_code == 201:
                self.logger.info('Customers successfully added to Customer API')
                return response.json() 
            else:
                self.logger.error(f"Error adding customers: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Communication error with Customer API: {str(e)}")
            return None
        
    def create_customer(self, name: str, plan_id: UUID, document: str = None) -> dict:
        """
        Creates a new customer in the Customer API.

        Args:
            name (str): The customer's name.
            plan_id (UUID): The subscription plan ID for the customer.
            document (str): The customer's document number.

        Returns:
            dict: The created customer as JSON or None if an error occurs.
        """
        try:
            self.logger.info(f'Sending request to create customer at {self.base_url}customer/create')
            payload = {
                "name": name,
                "plan_id": plan_id,
                "document": document
            }
            
            response = requests.post(f'{self.base_url}customer/create', data=payload)

            if response.status_code == HTTPStatus.CREATED:
                self.logger.info('Customer successfully created in Customer API')
                return response.json()
            else:
                self.logger.error(f"Error creating customer: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Communication error with Customer API: {str(e)}")
            return None