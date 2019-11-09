class Lexema(object):
    token: str
    classification: str
    line: int

    def __init__(self, token, classification, line):
        self.token = token
        self.classification = classification
        self.line = line
