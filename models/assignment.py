class Assignment:
    def __init__(self, name, details, mark, tests, infos):
        self.name = name
        self.details = details
        self.mark = mark
        self.tests = tests
        self.infos = infos

class Test:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

class Info:
    def __init__(self, keyword, message, min_num):
        self.keyword = keyword
        self.message = message
        self.min_num = min_num