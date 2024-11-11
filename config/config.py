import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        environment = os.getenv('FLASK_ENV')

        if environment == 'local':
            load_dotenv(dotenv_path='.env.local')
        elif environment == 'test':
            load_dotenv(dotenv_path='.env.test')
        else:
            load_dotenv(dotenv_path='.env')

        self.ENVIRONMENT = environment
        self.APP_NAME=os.getenv('APP_NAME')
        self.URL_REPORTS_SERVICE=os.getenv('URL_REPORTS_SERVICE')
        self.CUSTOMER_API_PATH=os.getenv('CUSTOMER_API_PATH')
        self.AUTH_API_PATH=os.getenv('AUTH_API_PATH')
        self.SECRET_KEY=os.getenv('SECRET_KEY')
        self.HOURS_TO_EXPIRE_SESSION=os.getenv('HOURS_TO_EXPIRE_SESSION')