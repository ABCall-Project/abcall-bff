
class IssueBuilder:
    def __init__(self):
        self.id = "28e6fc61-c101-4705-bc3d-e1752355762a"
        self.auth_user_id = "f7d0b546-94cb-468f-acf9-a3f287ba1b77"
        self.status = "Created"
        self.subject = "Problemas de funcionalidad"
        self.description = "Lorem Ipsum 668"
        self.created_at = "2023-10-23 05:00:00+00:00"
        self.closed_at = "2024-01-26 05:00:00+00:00"
        self.channel_plan_id = "3a46cc3e-b2ee-4aa0-8498-163e04eb1430"

    def with_id(self, id):
        self.id = id
        return self

    def with_auth_user_id(self, auth_user_id):
        self.auth_user_id = auth_user_id
        return self

    def with_status(self, status):
        self.status = status
        return self

    def with_subject(self, subject):
        self.subject = subject
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_created_at(self, created_at):
        self.created_at = created_at
        return self

    def with_closed_at(self, closed_at):
        self.closed_at = closed_at
        return self

    def with_channel_plan_id(self, channel_plan_id):
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
