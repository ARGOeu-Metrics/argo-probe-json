class Status:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    STATUS_STRING = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]

    def __init__(self):
        self._code = self.OK
        self._msg = ""

    def ok(self, msg):
        if self._code not in [self.WARNING, self.CRITICAL, self.UNKNOWN]:
            self._msg = f"{self.STATUS_STRING[self.OK]} - {msg}"
            self._code = self.OK

    def warning(self, msg):
        if self._code not in [self.CRITICAL, self.UNKNOWN]:
            self._msg = f"{self.STATUS_STRING[self.WARNING]} - {msg}"
            self._code = self.WARNING

    def critical(self, msg):
        self._msg = f"{self.STATUS_STRING[self.CRITICAL]} - {msg}"
        self._code = self.CRITICAL

    def unknown(self, msg):
        if self._code != self.CRITICAL:
            self._msg = f"{self.STATUS_STRING[self.UNKNOWN]} - {msg}"
            self._code = self.UNKNOWN

    def get_code(self):
        return self._code

    def get_msg(self):
        return self._msg.strip()
