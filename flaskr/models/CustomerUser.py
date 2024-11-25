from uuid import UUID
from datetime import datetime


class CustomerUser:
    def __init__(self, name: str, last_name: str, phone_number:str, email:str, address: str, birthdate:datetime, role_id:str, password: str, document:str, plan_id: UUID):
        self.name = name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthdate = birthdate
        self.role_id = role_id
        self.password = password
        self.document = document
        self.plan_id = plan_id

    def to_dict(self):
        return {
            "name": str(self.name),
            "last_name": str(self.last_name),
            "phone_number": str(self.phone_number),
            "email": str(self.email),
            "address": str(self.address),
            "birthdate": self.birthdate.strftime("%Y-%m-%d") if self.birthdate else None,
            "role_id": str(self.role_id),
            "password": self.password,
            "document": str(self.document),
            "plan_id": str(self.plan_id)
        }