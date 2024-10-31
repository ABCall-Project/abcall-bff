class InvoiceDataResponseBuilder:
    def __init__(self):
        self.id = "d0d2b83d-0188-45de-aecb-305e56237f22"
        self.auth_user_id = "e8b8a5d2-0f71-4e4d-b6e3-9c9d64f9cdda"
        self.status = "Created"
        self.subject = "Incidente por chatbot"
        self.description = "Hi"
        self.created_at = "2024-10-24 14:46:49.541187+00:00"
        self.closed_at = "2024-10-24 14:46:49.563244+00:00"
        self.channel_plan_id = "27d97115-18e6-4245-a2e0-723dca4e2a2d"

    def with_id(self, id: str):
        self.id = id
        return self

    def with_auth_user_id(self, auth_user_id: str):
        self.auth_user_id = auth_user_id
        return self

    def with_status(self, status: str):
        self.status = status
        return self

    def with_subject(self, subject: str):
        self.subject = subject
        return self

    def with_description(self, description: str):
        self.description = description
        return self

    def with_created_at(self, created_at: str):
        self.created_at = created_at
        return self

    def with_closed_at(self, closed_at: str):
        self.closed_at = closed_at
        return self

    def with_channel_plan_id(self, channel_plan_id: str):
        self.channel_plan_id = channel_plan_id
        return self

    def build(self):
        return {
            "id": self.id,
            "auth_user_id": self.auth_user_id,
            "status": self.status,
            "subject": self.subject,
            "description": self.description,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "channel_plan_id": self.channel_plan_id
        }
