from flask_restful import Resource, Api
from flask import Flask, request, json
from .utils.json_custom_encoder import JSONCustomEncoder
import requests
from flaskr import create_app
from config import Config
from .endpoint import HealthCheck,InvoiceView,ReportView,IssueView, CustomerDatabaseView,AuthUser
from flask_cors import CORS

config = Config()

app = create_app('default')
CORS(app)
app.json_encoder = JSONCustomEncoder

app_context = app.app_context()
app_context.push()

api = Api(app)

#resources
api.add_resource(HealthCheck, '/health')
api.add_resource(InvoiceView, '/invoices/<string:action>')
api.add_resource(ReportView, '/invoice/<string:invoice_id>')
api.add_resource(IssueView, '/issues/<string:action>')
api.add_resource(CustomerDatabaseView, '/customer/loadCustomerDataBase')
api.add_resource(AuthUser, '/auth/<string:action>')