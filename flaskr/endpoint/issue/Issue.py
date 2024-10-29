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
        elif action == 'getIssuesDashboard':
            return self.getIssuesDashboard()
        elif action == 'find':
            return self.get_issue_by_user_id()
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

    def getIssuesDashboard(self):
        try:
            self.logger.info(f'Receive request to get issues dashboard')

            customer_id = request.args.get('customer_id')
            status = request.args.get('status')
            channel_plan_id = request.args.get('channel_plan_id')
            created_at = request.args.get('created_at')
            closed_at = request.args.get('closed_at')

            issues = self.issue_service.get_issues_dashboard(
                customer_id=customer_id,
                status=status,
                channel_plan_id=channel_plan_id,
                created_at=created_at,
                closed_at=closed_at
            )

            if not issues:
                return {"message": "No issues found"}, HTTPStatus.NOT_FOUND

            return issues, HTTPStatus.OK

        except Exception as ex:
            self.logger.error(f'Some error occurred trying to get issues dashboard: {ex}')
            return {'message': 'Something went wrong trying to get issues dashboard'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    def get_issue_by_user_id(self):
        try:
            user_id = request.args.get('user_id')
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))

            self.logger.info(f'Receiving issue list by user {user_id}')

            issues = self.issue_service.get_issue_by_user_id(user_id=user_id, page=page, limit=limit)

            if issues:
                return issues, HTTPStatus.OK
            
            return [], HTTPStatus.NOT_FOUND

        except Exception as ex:
            self.logger.error(f'Some error ocurred trying to get issues by user id: {ex}')
            return {"message": "Some error ocurred trying to get issues by user id"}, HTTPStatus.INTERNAL_SERVER_ERROR
        