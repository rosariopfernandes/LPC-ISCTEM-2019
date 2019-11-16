class MethodCall(object):
    method_name: str
    arguments: list

    def __init__(self, method_name: str, arguments: list):
        self.method_name = method_name
        self.arguments = arguments

    def to_dict(self):
        _dict = {'method_name': self.method_name}
        _dict_arguments = []
        for argument in self.arguments:
            _dict_arguments.append(argument)
