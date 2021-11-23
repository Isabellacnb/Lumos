# ------------ function_directory.py ------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Function
# -----------------------------------------------

class Function:
    def __init__(self, name, type, parameters, quadruplePosition, memoryLimits):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.quadruplePosition = quadruplePosition
        self.limits = memoryLimits
    
    def __str__(self):
        return "Function: " + str(self.name) + " (" + str(self.type) + ") - " + str(self.parameters) + " - " + str(self.quadruplePosition) + "(quad position)" + str(self.limits)