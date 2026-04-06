class InsufficientStockError(Exception):
    """Raised when a user tries to withdraw more than their balance."""
    def __init__(self, message="Insufficient stock"):
        self.message = message
        super().__init__(self.message)