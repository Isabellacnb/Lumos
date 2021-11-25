# ------------ quadruple.py ------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Quadruple
# Structure that represents a quadruple
# operator - leftOperand - rightOperand - result
# --------------------------------------------------

class Quadruple():
    def __init__(self, operator, operLeft, operRight, result):
        self.operator = operator
        self.operLeft = operLeft
        self.operRight = operRight
        self.result = result
    
    def __str__(self):
        return "(" + str(self.operator) + ", " + str(self.operLeft) + ", " + str(self.operRight) + ", " + str(self.result) + ")"