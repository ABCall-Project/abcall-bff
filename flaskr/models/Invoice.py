from uuid import UUID
from typing import Optional
from datetime import datetime

class Invoice:
    """
    This class represent the invoice
    Attributes:
        id (uniqueidentifier): id invoice
        customer_id (UUID): id customer invoice
        invoice_id (str): invoice number
        plan_id (Optional[UUID]): id plan
        amount (float): amount invoice
        tax (float): value of taxes
        total_amount (float): total amount
        status (str): invoice status
        created_at (datetime): creation date
        start_at (datetime): start date
        generation_date (datetime): generation date
        end_at (datetime): end date invoice
        plan_amount (float): value of plan
        issues_amout (float): cost by issues
    """
    def __init__(self, id: UUID, customer_id: UUID, invoice_id: str, plan_id: UUID, amount: float, tax: float,
                 total_amount: float, status: str,
                 created_at: datetime, start_at: str, generation_date: datetime, end_at: str, plan_amount:float, issues_amount:float):
        self.id = id
        self.customer_id = customer_id
        self.invoice_id = invoice_id
        self.plan_id = plan_id
        self.amount = amount
        self.tax = tax
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.start_at = start_at
        self.generation_date = generation_date
        self.end_at = end_at
        self.plan_amount=plan_amount
        self.issues_amount=issues_amount



    def to_dict(self):
        return {
            'id': str(self.id),
            'customerId': str(self.customer_id),
            'invoiceId': str(self.invoice_id),
            'planId': str(self.plan_id) if self.plan_id else None,
            'amount': self.amount,
            'tax': self.tax,
            'totalAmount': self.total_amount,
            'status': self.status,
            'createdAt': self.created_at if self.created_at else None,
            'startAt': self.start_at if self.start_at else None,
            'generationDate': self.generation_date if self.generation_date else None,
            'end_at': self.end_at if self.end_at else None,
            'planAmount':self.plan_amount,
            'issuesAmount':self.issues_amount
        }