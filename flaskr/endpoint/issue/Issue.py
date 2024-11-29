import json
from flask_restful import Resource
from flask import jsonify, request
from http import HTTPStatus
from ...service.IssueService import *
import logging
from ...middleware.AuthMiddleware import token_required

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

    @token_required
    def get(self, action=None):
        if action == 'getIAResponse':
            return self.getIAResponse()
        elif action == 'find':
            return self.get_issue_by_user_id()
        elif action == 'getIssuesDasboard':
            return self.getIssuesDasboard()
        elif action=='getIAPredictiveAnswer':
            return self.get_ia_predictive_answer()
        elif action=='get_issue_by_id':
            return self.get_issue_detail()
        elif action == 'getAllIssues':
            return self.get_all_issues()
        elif action == 'getOpenIssues':
            return self.get_open_issues()
        elif action == 'getTopSevenIssues':
            return self.get_top_seven_issues()
        elif action == 'getPredictedData':
            return self.get_predicted_data()
        else:
            return {"message": "Action not found"}, 404
    
    def post(self,action=None):
        if action == 'assignIssue':
            return self.assign_issue()
        elif action == 'createIssue':
            return self.create_issue()
        elif action == 'processEmails':
            return self.process_emails()
        else:
            return {"message": "Action not found"}, 404

    def process_emails(self):
        """
        Trigger email processing to create issues.
        """
        self.logger.info("Processing incoming emails for issues.")
        try:
            self.issue_service.process_incoming_emails()
            return {"message": "Emails processed successfully."}, HTTPStatus.OK
        except Exception as ex:
            self.logger.error(f"Error processing emails: {ex}")
            return {"message": "Error processing emails."}, HTTPStatus.INTERNAL_SERVER_ERROR

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
            
            return {}, HTTPStatus.NOT_FOUND

        except Exception as ex:
            self.logger.error(f'Some error ocurred trying to get issues by user id: {ex}')
            return {"message": "Some error ocurred trying to get issues by user id"}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def get_ia_predictive_answer(self):
        try:

            self.logger.info(f'Receive request to ask to predictive ai')
            user_id = request.args.get('user_id')
            answer=self.issue_service.get_ia_predictive_answer(user_id)
            return {
                'answer': answer
            }, HTTPStatus.OK
            
        except Exception as ex:
            self.logger.error(f'Some error occurred trying ask predictive ai: {ex}')
            return {'message': 'Something was wrong trying ask predictive ai'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_issue_detail(self):
            try:
                # Obtener `customer_id` e `issue_id` de los parámetros de la solicitud
                customer_id = request.args.get('customer_id')
                issue_id = request.args.get('issue_id')

                self.logger.info(f'Receive request to get issue detail for customer_id {customer_id} and issue_id {issue_id}')

                # Llamar al servicio para obtener el detalle del issue
                issue_detail = self.issue_service.get_issue_detail(customer_id=customer_id, issue_id=issue_id)

                if issue_detail:
                    return issue_detail, HTTPStatus.OK
                else:
                    return {"message": "Issue not found"}, HTTPStatus.NOT_FOUND

            except Exception as ex:
                self.logger.error(f'Some error occurred trying to get issue detail: {ex}')
                return {'message': 'Something went wrong trying to get issue detail'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_all_issues(self):
            try:
                user_id = request.args.get('user_id')
                self.logger.info(f'Receiving issue list by user {user_id}')

                issues = self.issue_service.get_all_issues()

                if issues:
                    return issues, HTTPStatus.OK
                
                return {}, HTTPStatus.NOT_FOUND

            except Exception as ex:
                self.logger.error(f'Some error ocurred trying to get all issues: {ex}')
                return {"message": "Some error ocurred trying to get all issues"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def assign_issue(self):
            try:
                self.logger.info(f'Receiving issue for  assign_issue')
                issue_id = request.args.get('issue_id')
                data = request.get_json()
                auth_user_agent_id = data.get('auth_user_agent_id')
                issues = self.issue_service.assign_issue(issue_id,auth_user_agent_id)
                if issues:
                    return issues, HTTPStatus.OK
                
                return {}, HTTPStatus.NOT_FOUND

            except Exception as ex:
                self.logger.error(f'Some error ocurred trying to assign_issue issues: {ex}')
                return {"message": "Some error ocurred trying to assign_issue issues"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_open_issues(self):
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))


            self.logger.info(f'Receiving issue get_open_issues')

            issues = self.issue_service.get_open_issues(page=page, limit=limit)

            if issues:
                return issues, HTTPStatus.OK
            
            return {}, HTTPStatus.NOT_FOUND

        except Exception as ex:
            self.logger.error(f'Some error ocurred trying to get issues by user id: {ex}')
            return {"message": "Some error ocurred trying to get issues by user id"}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def get_top_seven_issues(self):
            try:
                self.logger.info(f'Receiving issue top seven issues')

                issues = self.issue_service.get_top_seven_issues()

                if issues:
                    return issues, HTTPStatus.OK
                
                return {}, HTTPStatus.NOT_FOUND

            except Exception as ex:
                self.logger.error(f'Some error ocurred trying to get top seven issues: {ex}')
                return {"message": "Some error ocurred trying to get top seven issues"}, HTTPStatus.INTERNAL_SERVER_ERROR
            
    def get_predicted_data(self):
        try:
            self.logger.info('Receiving issue predicted data')

            issues = self.issue_service.get_predicted_data()

            if issues:
                return issues, HTTPStatus.OK
            
            return {}, HTTPStatus.NOT_FOUND

        except Exception as ex:
            self.logger.error(f'Some error ocurred trying to get predicted data: {ex}')
            return {"message": "Some error ocurred trying to get predicted data"}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    def create_issue(self):
        """
        Handles the creation of a new issue.
        """
        self.logger.info('Received request to create an issue.')
        try:
            file = request.files.get('file')
            data = request.get_json() if request.is_json else request.form.to_dict()

            auth_user_id = data.get("auth_user_id")
            auth_user_agent_id = data.get('auth_user_agent_id')
            subject = data.get("subject")
            description = data.get("description")

            self.logger.info(f"Creating issue for user ID: {auth_user_id}")

            file_path = None
            if file:
                upload_directory = os.path.join(os.getcwd(), 'uploads')
                os.makedirs(upload_directory, exist_ok=True)
                file_path = os.path.join(upload_directory, file.filename)
                file.save(file_path)
                self.logger.info(f"File uploaded successfully at {file_path}")

            self.issue_service.create_issue(
                auth_user_id=auth_user_id,
                auth_user_agent_id=auth_user_agent_id,
                subject=subject,
                description=description,
                file_path=file_path
            )

            return {"message": "Issue created successfully"}, HTTPStatus.CREATED

        except Exception as ex:
            self.logger.error(f"Error while creating issue: {ex}")
            return {"message": "Error creating issue"}, HTTPStatus.INTERNAL_SERVER_ERROR    