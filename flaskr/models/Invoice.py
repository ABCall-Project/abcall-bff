class Invoice:
    """
    This class represent the invoice
    Attributes:
        id (uniqueidentifier) id invoice
        number_id (int) number of invoice
        generated_date (data) date of invoice
        period (string) period of invoice
        mount (decimal) invoice mount to pay
        state (string) state of invoice, paid or pending 
        url_document (byte) url of invoice to download
    """
    def __init__(self,id,number_id, generated_date, period, mount, state, url_document):
        self.id=id
        self.number_id=number_id
        self.generated_date=generated_date
        self.period=period
        self.mount=mount
        self.state=state
        self.url_document=url_document