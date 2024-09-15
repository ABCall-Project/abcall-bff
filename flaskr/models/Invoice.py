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
        payment_id (Optional[UUID]): id payment
        amount (float): amount invoice
        tax (float): value of taxes
        total_amount (float): total amount
        subscription (str): suscription name
        subscription_id (UUID): suscription id
        status (str): invoice status
        created_at (datetime): creation date
        updated_at (datetime): update date
        generation_date (datetime): generation date
        period (datetime): period invoice
    """
    def __init__(self, id: UUID, customer_id: UUID, invoice_id: str, payment_id: Optional[UUID], amount: float, tax: float,
                 total_amount: float, subscription: str, subscription_id: UUID, status: str,
                 created_at: datetime, updated_at: datetime, generation_date: datetime, period: datetime):
        self.id = id
        self.customer_id = customer_id
        self.invoice_id = invoice_id
        self.payment_id = payment_id
        self.amount = amount
        self.tax = tax
        self.total_amount = total_amount
        self.subscription = subscription
        self.subscription_id = subscription_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.generation_date = generation_date
        self.period = period

    def to_dict(self):
        return {
            'id': str(self.id),
            'customerId': str(self.customer_id),
            'invoiceId': str(self.invoice_id),
            'paymentId': str(self.payment_id) if self.payment_id else None,
            'amount': self.amount,
            'tax': self.tax,
            'totalAmount': self.total_amount,
            'subscription': self.subscription,
            'subscriptionId': str(self.subscription_id),
            'status': self.status,
            'createdAt': self.created_at if self.created_at else None,
            'updatedAt': self.updated_at if self.updated_at else None,
            'generationDate': self.generation_date if self.generation_date else None,
            'period': self.period if self.period else None
        }