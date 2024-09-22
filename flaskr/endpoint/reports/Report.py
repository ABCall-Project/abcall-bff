import json
from flask_restful import Resource
from flask import jsonify, request,Response
from http import HTTPStatus
import logging
from ...service.ReportService import ReportService

class ReportView(Resource):
    """
    This class represent a reports service view
    Attributes:
        na
    """

    def get(self, invoice_id):
        """
        This method is to download a invoice from her id

        Args:
            invoice_id (str): invoice id
        
        Returns:
            JSON reponse contain the byte array of invoice
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'receiving request to download invoice : {invoice_id}')
        try:
            
            report_service=ReportService()
            content=report_service.download_invoice_by_id(invoice_id)
            if content:
                response = Response(content, mimetype='application/octet-stream')

                    
                response.headers.set('Content-Disposition', 'attachment', filename=f'invoice-{invoice_id}.pdf')

                return response
            else:
                return 'Invoice not found', HTTPStatus.NOT_FOUND
        except Exception as ex:
            self.logger.error(f'Some error occurred trying to download invoice {invoice_id}: {ex}')
            return {'message': 'Something was wrong trying download invoice'}, HTTPStatus.INTERNAL_SERVER_ERROR
        


