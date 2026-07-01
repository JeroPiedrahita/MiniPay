class CreatePaymentDTO:
    """
    Data Transfer Object (DTO) for payment creation.
    
    Attributes:
        amount (float): The total amount of the transaction.
        currency (str): The currency type (e.g., USD, COP).
        source_account (str): The origin account number.
        destination_account (str): The recipient account number.
    """
    def __init__(self, amount: float, currency: str, source_account: str, destination_account: str):
        self.amount = amount
        self.currency = currency
        self.source_account = source_account
        self.destination_account = destination_account