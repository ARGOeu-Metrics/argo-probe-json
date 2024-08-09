class JsonException(Exception):
    def __init__(self, msg):
        self.msg = msg


class WarningException(JsonException):
    def __str__(self):
        return str(self.msg)


class CriticalException(JsonException):
    def __str__(self):
        return str(self.msg)
