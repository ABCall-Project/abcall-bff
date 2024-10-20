from uuid import UUID
from typing import Optional
from datetime import datetime

class InvoiceDetail:
    def __init__(self, id: UUID, detail: str, invoice_id: UUID, issue_id: Optional[UUID], amount: float, tax: float,
                 total_amount: float, chanel_plan_id: UUID,issue_date:datetime=None):
        self.id = id
        self.detail=detail
        self.amount=amount
        self.tax=tax
        self.total_amount=total_amount
        self.issue_id=issue_id
        self.chanel_plan_id=chanel_plan_id
        self.invoice_id=invoice_id
        self.issue_date=issue_date

    def to_dict(self):
        return {
            'id': str(self.id),
            'detail': str(self.detail),
            'amount': str(self.amount),
            'tax': str(self.tax),
            'totalAmount': str(self.total_amount),
            'issueId': str(self.issue_id),
            'chanelPlanId': str(self.chanel_plan_id),
            'invoiceId': str(self.invoice_id),
            'issueDate': self.issue_date if self.issue_date else None
        }