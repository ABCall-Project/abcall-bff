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
