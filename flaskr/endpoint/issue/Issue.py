import json
from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...service.IssueService import *
import logging

class IssueView(Resource):
    """
    This class represent a invoce api view
    Attributes:
        na
    """

    def __init__(self):
        self.issue_service = IssueService()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')


    def get(self, action=None):
        if action == 'getIAResponse':
            return self.getIAResponse()
        if action == 'getIssuesDasboard':
            return self.getIssuesDasboard()
        else:
            return {"message": "Action not found"}, 404

    def getIAResponse(self):
        try:

            self.logger.info(f'Receive request to ask to open ai')
            question = request.args.get('question')
            answer=self.issue_service.get_answer_ai(question)
            return {
                'answer': answer
            }, HTTPStatus.OK
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying ask open ai: {ex}')
            return {'message': 'Something was wrong trying ask open ai'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def getIssuesDasboard(self):
        """
        This method is to query issues for a customer with optional filters.

        Args: 
            customer_id (UUID): customer id
        Returns:
            JSON response containing the issues or an error message.
        """
        customer_id = request.args.get('customer_id')

        self.logger.info(f'Receiving request to query issues for customer id: {customer_id}')

        issues = self.issue_service.get_issues_dashboard(
            customer_id=customer_id,
            status=request.args.get('status'),
            channel_plan_id=request.args.get('channel_plan_id'),
            created_at=request.args.get('created_at'),
            closed_at=request.args.get('closed_at')
        )

        if not issues:
            return {"message": "No issues found"}, HTTPStatus.NOT_FOUND

        issues_list = [issue.to_dict() for issue in issues]

        return issues_list, HTTPStatus.OK