from uuid import UUID
from datetime import datetime
from typing import Optional

class Customer:
    """
    This class represents a customer.
    
    Attributes:
        id (UUID): Unique identifier for the customer.
        document (str): Identification document of the customer.
        name (str): Full name of the customer.
        plan_id (UUID): Identifier for the customer's subscription plan.
        date_suscription (datetime): Date and time when the subscription was created.
    """
    
    def __init__(self, id: UUID, document: str, name: str, plan_id: UUID, date_suscription: Optional[datetime] = None):
        self.id = id
        self.document = document
        self.name = name
        self.plan_id = plan_id
        self.date_suscription = date_suscription or datetime.now()

    def to_dict(self):
        """
        Method to convert the customer object into a dictionary.
        """
        return {
            'id': str(self.id),
            'document': self.document,
            'name': self.name,
            'plan_id': str(self.plan_id),
            'date_suscription': self.date_suscription.isoformat() if self.date_suscription else None
        }