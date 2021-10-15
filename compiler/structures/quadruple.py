class Quadruple():
    def __init__(self, operator, oper_one, oper_two, result):
        self.operator = operator
        self.oper_one = oper_one
        self.oper_two = oper_two
        self.result = result
    
    def __str__(self):
        return "(" + self.operator + ", " + self.oper_one + ", " + self.oper_two + ", " + self.result + ")"