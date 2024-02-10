class SuccessResponse:
    def __init__(self, data=None, message="Success"):
        self.status = "success"
        self.message = message
        self.data = data
