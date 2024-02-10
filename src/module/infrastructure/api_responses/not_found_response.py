class NotFoundResponse:
    def __init__(self, message="Not Found", errors=None):
        self.status = "not_found"
        self.message = message
        self.errors = errors
