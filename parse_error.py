class ParseError(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.__str__())

    def __str__(self):
        if self.token is None:
            return self.message

        line = getattr(self.token, "line", None)
        column = getattr(self.token, "column", None)
        location = f"{line}:{column}" if line is not None and column is not None else "?:?"
        return f"{self.message} en {location} (token: {self.token.type} '{self.token.value}')"