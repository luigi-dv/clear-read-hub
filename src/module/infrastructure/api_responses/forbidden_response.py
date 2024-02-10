class ForbiddenResponse:
    def __init__(self, message="Forbidden", errors=None):
        self.status = "forbidden"
        self.message = message
        self.errors = errors
