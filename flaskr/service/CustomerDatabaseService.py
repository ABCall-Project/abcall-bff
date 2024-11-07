from datetime import date
from uuid import UUID
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging

class CustomerDatabaseService:
    """
    This class is for integrating the BFF with the CustomerDatabase API.
    Attributes:
        base_url (string): the CustomerDatabase API URL.
    """

    def __init__(self):
        """
        Service constructor.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instancing CustomerDatabase service')
        self.base_url = os.environ.get('CUSTOMER_API_PATH')
        self.logger.info(self.base_url)

    def load_entries(self, customer_id: UUID, entries: list) -> list:
        """
        Loads entries into the customer database.

        Args:
            customer_id (UUID): The customer ID associated with each entry.
            entries (list): List of dictionaries with 'topic' and 'content' for each entry.

        Returns:
            list: List of loaded entries as JSON or None if an error occurs.
        """
        try:
            self.logger.info(f'Sending request to load entries at {self.base_url}/customer/loadCustomerDataBase')
            payload = {
                "customer_id": str(customer_id),
                "entries": entries
            }
            response = requests.post(f'{self.base_url}/customer/loadCustomerDataBase', json=payload)

            if response.status_code == 201:
                self.logger.info('Entries successfully loaded into customer database')
                return response.json()  # Retorna el JSON directamente para que el BFF lo interprete
            else:
                self.logger.error(f"Error loading entries: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Communication error with CustomerDatabase API: {str(e)}")
            return None