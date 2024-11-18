from flask_restful import Resource
from flask import request, jsonify
from http import HTTPStatus
from ...service.CustomerService import CustomerService
from uuid import UUID
import logging
from ...middleware.AuthMiddleware import token_required

class CustomerView(Resource):
    """
    This class provides an endpoint to manage customer-related operations.
    """

    def __init__(self):
        self.customer_service = CustomerService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
    
    def post(self):
        try:
            data = request.get_json()
            plan_id = data.get("plan_id")
            customers = data.get("customers", [])

            self.logger.info(f'Adding {len(customers)} customers with plan ID: {plan_id}')
            
            result = self.customer_service.add_customers(customers, UUID(plan_id))

            if result is not None:
                return result, HTTPStatus.CREATED
            else:
                return {"message": "Failed to add customers"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as ex:
            self.logger.error(f"Error adding customers: {ex}")
            return {'message': 'An error occurred while adding customers'}, HTTPStatus.INTERNAL_SERVER_ERROR
