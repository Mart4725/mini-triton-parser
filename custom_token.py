class Token:
    def __init__(self, type_, value, error=None, line=None, column=None):
        self.type = type_
        self.value = value
        self.error = error
        self.line = line
        self.column = column

    def clean(self, v):
        if v is None:
            return "—"
        return str(v)

    def __repr__(self):
        return f"{self.type:>10} | {self.clean(self.value):>10} | {self.clean(self.error):>25} | {self.line}:{self.column}"