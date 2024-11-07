from flask_restful import Resource
from flask import request, jsonify
from http import HTTPStatus
from ...service.CustomerDatabaseService import CustomerDatabaseService
from uuid import UUID
import logging

class CustomerDatabaseView(Resource):
    """
    This class provides an endpoint to load entries for a customer in the Customer Database.
    """

    def __init__(self):
        self.customer_database_service = CustomerDatabaseService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')

    def post(self):
        try:
            data = request.get_json()
            customer_id = data.get("customer_id")
            entries = data.get("entries", [])

            self.logger.info(f'Loading entries for customer ID: {customer_id}')
            
            # Llama al servicio
            result = self.customer_database_service.load_entries(UUID(customer_id), entries)

            # Solo para diagnóstico
            if result is not None:
                return result, HTTPStatus.CREATED
            else:
                return {"message": "Failed to load entries"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as ex:
            self.logger.error(f"Error loading entries for customer: {ex}")
            return {'message': 'An error occurred while loading entries'}, HTTPStatus.INTERNAL_SERVER_ERROR
