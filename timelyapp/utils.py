class AppResponse:
    def __init__(self, error, error_message, success_message, data):
        self.error = error
        self.error_message = error_message
        self.success_message = success_message
        self.data = data