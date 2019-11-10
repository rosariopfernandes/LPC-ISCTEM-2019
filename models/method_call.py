class MethodCall(object):
    method_name: str
    arguments: list

    def __init__(self, method_name: str, arguments: list):
        self.method_name = method_name
        self.arguments = arguments
