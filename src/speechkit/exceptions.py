"""Basic speechkit exceptions."""


class RequestError(Exception):
    """Exception raised for errors while yandex api request"""

    def __init__(self, answer: dict, *args):
        self.error_code = str(answer.get('code', '')) + str(answer.get('error_code', ''))
        self.message = str(answer.get('message', '')) + str(answer.get('error_message', ''))
        if self.error_code + self.message == '':
            self.message = str(answer)

        super().__init__(self.error_code + ' ' + self.message, *args)
