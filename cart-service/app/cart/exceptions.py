class ProductNotFoundError(Exception):
    """Raised when the Product Service returns a 404."""
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} was not found in the Product Service.")

class NotAvailebleInStokError(Exception):
    """Raised when the Product Service returns a 404."""
    def __init__(self, message="Not enough stock available"):
        self.message = message
        super().__init__(message)