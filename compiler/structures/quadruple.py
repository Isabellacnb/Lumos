class Quadruple():
    def __init__(self, operator, operLeft, operRight, result):
        self.operator = operator
        self.operLeft = operLeft
        self.operRight = operRight
        self.result = result
    
    def __str__(self):
        return "(" + self.operator + ", " + self.operLeft + ", " + self.operRight + ", " + self.result + ")"