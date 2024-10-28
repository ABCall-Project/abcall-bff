from uuid import UUID
from flaskr.models.Invoice import Invoice
from datetime import datetime

class InvoiceResponseBuilder:
    def __init__(self):
        self.id = "7a0d0170-aa1c-4bc3-815b-7b17de4cd50e"
        self.customerId = "f296041a-4480-4ebe-8a75-2dd0696d58e8"
        self.invoiceId="f296041a-4480-4ebe-8a75-2dd0696d58e8"
        self.planId = "7a0d0170-aa1c-4bc3-815b-7b17de4cd50e"
        self.amount = 300.0
        self.tax= 513
        self.totalAmount = 3213
        self.status = "PENDING"
        self.createdAt = "2024-10-27T11:34:43"
        self.startAt = "2024-10-27T11:34:43"
        self.generationDate = "2024-10-27T14:34:43"
        self.end_at = "2024-10-27T14:34:43"
        self.planAmount = 1500
        self.issuesAmount= 900.0
    
    def with_id(self, id:UUID):
        self.id = id
        return self

    def with_customerId(self, customerId:str):
        self.customerId = customerId
        return self

    def with_invoiceId(self,invoiceId:str):
        self.invoiceId = invoiceId
        return self
    
    def with_planId(self,planId:str):
        self.planId = planId
        return self
    
    def with_amount(self,amount:float):
        self.amount = amount
        return self
    
    def with_tax(self,tax:float):
        self.tax = tax
        return self
    
    def with_totalAmount(self,totalAmount:float):
        self.totalAmount = totalAmount
        return self
    
    def with_status(self,status:str):
        self.status = status
        return self
    
    def with_createdAt(self,createdAt:str):
        self.createdAt = createdAt
        return self
    
    def with_startAt(self,startAt:str):
        self.startAt = startAt
        return self
    
    def with_generationDate(self,generationDate:str):
        self.generationDate = generationDate
        return self
    

    def with_end_at(self,end_at:datetime):
        self.end_at = end_at
        return self
    
    def with_planAmount(self,planAmount:float):
        self.planAmount = planAmount
        return self
    
    def with_issuesAmount(self,issuesAmount:float):
        self.issuesAmount = issuesAmount
        return self

    
    def build(self):
        return {
            'id': self.id,
            'customerId': self.customerId,
            'invoiceId': self.invoiceId,
            'planId': self.planId,
            'amount': self.amount,
            'tax': self.tax,
            'totalAmount': self.totalAmount,
            'status': self.status,
            'createdAt': self.createdAt,
            'startAt': self.startAt,
            'generationDate': self.generationDate,
            'endAt': self.end_at,
            'plan_amount':self.planAmount,
            'issues_amount':self.issuesAmount
        }