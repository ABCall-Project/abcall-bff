import unittest
from datetime import datetime
from uuid import uuid4
from flaskr.models.auth import Auth

class AuthModelTest(unittest.TestCase):
    def setUp(self):

        self.auth_id = uuid4()
        self.name = "John"
        self.last_name = "Doe"
        self.phone_number = "1234567890"
        self.email = "john.doe@example.com"
        self.address = "123 Main St"
        self.birthdate = datetime(1990, 1, 1)
        self.role_id = "admin"
        self.token = "some_token_string"

      
        self.auth = Auth(
            id=self.auth_id,
            name=self.name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            email=self.email,
            address=self.address,
            birthdate=self.birthdate,
            role_id=self.role_id,
            token=self.token
        )

    def test_initialization(self):
        
        self.assertEqual(self.auth.id, self.auth_id)
        self.assertEqual(self.auth.name, self.name)
        self.assertEqual(self.auth.last_name, self.last_name)
        self.assertEqual(self.auth.phone_number, self.phone_number)
        self.assertEqual(self.auth.email, self.email)
        self.assertEqual(self.auth.address, self.address)
        self.assertEqual(self.auth.birthdate, self.birthdate)
        self.assertEqual(self.auth.role_id, self.role_id)
        self.assertEqual(self.auth.token, self.token)

    def test_to_dict(self):
        
        auth_dict = self.auth.to_dict()

        self.assertEqual(auth_dict["id"], str(self.auth_id))
        self.assertEqual(auth_dict["name"], self.name)
        self.assertEqual(auth_dict["last_name"], self.last_name)
        self.assertEqual(auth_dict["phone_number"], self.phone_number)
        self.assertEqual(auth_dict["email"], self.email)
        self.assertEqual(auth_dict["address"], self.address)
        self.assertEqual(auth_dict["birthdate"], self.birthdate)
        self.assertEqual(auth_dict["role_id"], self.role_id)
        self.assertEqual(auth_dict["token"], self.token)
