from uuid import UUID
from datetime import datetime
from typing import Optional

class CustomerDatabase:
    """
    This class represents an entry in the customer database.
    
    Attributes:
        id (UUID): Unique identifier for the entry.
        customer_id (UUID): Identifier for the customer associated with the entry.
        topic (str): Topic or subject of the entry.
        content (str): Detailed content or information related to the topic.
        created_at (datetime): Date and time when the entry was created.
    """
    
    def __init__(self, id: UUID, customer_id: UUID, topic: str, content: str, created_at: Optional[datetime] = None):
        self.id = id
        self.customer_id = customer_id
        self.topic = topic
        self.content = content
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """
        Method to convert the customer database entry object into a dictionary.
        """
        return {
            'id': str(self.id),
            'customer_id': str(self.customer_id),
            'topic': self.topic,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }