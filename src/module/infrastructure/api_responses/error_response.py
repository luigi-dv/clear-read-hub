class ErrorResponse:
    def __init__(self, message="An error occurred", errors=None):
        self.status = "error"
        self.message = message
        self.errors = errors
