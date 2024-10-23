from uuid import UUID
from datetime import datetime
from typing import Optional

class Issue:
    """
    This class represents an issue reported by a customer.
    Attributes:
        id (UUID): Unique identifier of the issue.
        auth_user_id (UUID): ID of the user who reported the issue.
        auth_user_agent_id (UUID): ID of the agent associated with the issue.
        status (str): Current status of the issue (e.g., open, closed).
        subject (str): Subject or title of the issue.
        description (str): Detailed description of the issue.
        created_at (datetime): Date and time when the issue was created.
        closed_at (Optional[datetime]): Date and time when the issue was closed (if applicable).
        channel_plan_id (Optional[UUID]): ID of the channel plan associated with the issue.
    """
    
    def __init__(self, id: UUID, auth_user_id: UUID, auth_user_agent_id: UUID, status: str, 
                 subject: str, description: str, created_at: datetime, closed_at: Optional[datetime], 
                 channel_plan_id: Optional[UUID]):
        self.id = id
        self.auth_user_id = auth_user_id
        self.auth_user_agent_id = auth_user_agent_id
        self.status = status
        self.subject = subject
        self.description = description
        self.created_at = created_at
        self.closed_at = closed_at
        self.channel_plan_id = channel_plan_id

    def to_dict(self):
        """
        Method to convert the issue object into a dictionary.
        """
        return {
            'id': str(self.id),
            'auth_user_id': str(self.auth_user_id),
            'auth_user_agent_id': str(self.auth_user_agent_id),
            'status': self.status,
            'subject': self.subject,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'channel_plan_id': str(self.channel_plan_id) if self.channel_plan_id else None
        }