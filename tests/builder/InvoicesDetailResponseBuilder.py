from uuid import UUID
from datetime import datetime
from flaskr.models.invoice_detail import InvoiceDetail


class InvoiceDetailResponseBuilder():
    def __init__(self):
        self.id = "1cd11f8b-209b-4e44-8791-a06747cb6f80"
        self.detail = "Lorem Ipsum"
        self.amount = 300.0
        self.tax = 57.0
        self.totalAmount = 357.0
        self.issueId = "9bca6144-ac5b-4e78-97f6-d1f2eeaa7619"
        self.chanelPlanId = "787f5517-290b-4c6a-a27d-2220581c2a26"
        self.invoiceId = "94b9f59f-a6a0-4d47-ae7a-ed725711cb6a"
        self.issueDate = "2024-10-27T11:34:43"

    def with_id(self, id: str):
        self.id = id
        return self

    def with_detail(self, detail: str):
        self.detail = detail
        return self

    def with_amount(self, amount: float):
        self.amount = amount
        return self

    def with_tax(self, tax: float):
        self.tax = tax
        return self

    def with_totalAmount(self, totalAmount: float):
        self.totalAmount = totalAmount
        return self

    def with_issueId(self, issueId: str):
        self.issueId = issueId
        return self

    def with_chanelPlanId(self, chanelPlanId: str):
        self.chanelPlanId = chanelPlanId
        return self

    def with_invoiceId(self, invoiceId: str):
        self.invoiceId = invoiceId
        return self

    def with_issueDate(self, issue_date: datetime):
        self.issue_date = issue_date
        return self

    def build(self):
        return {
            "id": self.id,
            "detail": self.detail,
            "amount": self.amount,
            "tax": self.tax,
            "totalAmount": self.totalAmount,
            "issueId": self.issueId,
            "chanelPlanId": self.chanelPlanId,
            "invoiceId": self.invoiceId,
            "issueDate": self.issueDate
        }
