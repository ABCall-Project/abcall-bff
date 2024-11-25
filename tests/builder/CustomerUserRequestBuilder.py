class CustomerUserRequestBuilder:
    def __init__(self):
        self.name = "John"
        self.last_name = "Doe"
        self.phone_number = "1234567890"
        self.email = "Lorem@email.com"
        self.address = "123 Main St"
        self.birthdate = "1990-01-01"
        self.role_id = "3a46cc3e-b2ee-4aa0-8498-163e04eb1430"
        self.document = "1234567890"
        self.plan_id = None

    def with_name(self, name):
        self.name = name
        return self

    def with_last_name(self, last_name):
        self.last_name = last_name
        return self

    def with_phone_number(self, phone_number):
        self.phone_number = phone_number
        return self

    def with_email(self, email):
        self.email = email
        return self

    def with_address(self, address):
        self.address = address
        return self

    def with_birthdate(self, birthdate):
        self.birthdate = birthdate
        return self

    def with_role_id(self, role_id):
        self.role_id = role_id
        return self
    
    def with_document(self, document):
        self.document = document
        return self
    
    def with_plan_id(self, plan_id):
        self.plan_id = plan_id
        return self

    def build(self):
        return {
            "name":self.name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "birthdate": self.birthdate,
            "role_id": self.role_id,
            "document": self.document,
            "plan_id": self.plan_id
        }
