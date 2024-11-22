from flaskr.models.Plan import Plan
class CustomerCreationResponseBuilder:
    def __init__(self):
        self.id = "3a46cc3e-b2ee-4aa0-8498-163e04eb1430"
        self.name = "DinoGeek"
        self.plan_id = Plan.ENTREPRENEUR
        self.document = "123"

    def with_id(self, id):
        self.id = id
        return self
    
    def with_name(self, name):
        self.name = name
        return self
    
    def with_plan_id(self, plan_id):
        self.plan_id = plan_id
        return self
    
    def with_document(self, document):
        self.document = document
        return self

    def build(self):
        return {
            "id": self.id,
            "name": self.name,
            "plan_id": self.plan_id,
            "document": self.document
        }